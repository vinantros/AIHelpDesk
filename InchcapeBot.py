import tkinter as tk
import openai
import customtkinter
import requests
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api import TranscriptsDisabled
from youtubesearchpython import VideosSearch
import threading
import msal
import requests
import json

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

openai.api_key = ""

class ChatBot:
    def __init__(self, root):

        self.root = root
        
        # Create a frame to hold the entry widget and send button
        self.frame = customtkinter.CTkFrame(self.root)
        
        # Create the sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self.root)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Add buttons to the sidebar frame
        self.weather_button = customtkinter.CTkButton(self.sidebar_frame, text="Weather", command=self.show_weather)
        self.weather_button.pack(side=tk.TOP, padx=10, pady=10)
        
        self.greeting_button = customtkinter.CTkButton(self.sidebar_frame, text="Summarize", command=self.youtube_summarize)
        self.greeting_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create the chatbox widget
        self.chatbox = tk.Text(self.root, height=20, width=50, wrap=tk.WORD)
        self.chatbox.configure(background='black')
        self.chatbox.configure(foreground='white')
        self.chatbox.configure(font=('TkDefaultFont', 14))
        self.chatbox.tag_configure("you_tag", foreground="#00ff00")
        self.chatbox.tag_configure("Captain_tag", foreground="#00ff00")
        self.chatbox.config(state=tk.DISABLED)  # Set the chatbox state to disabled (read-only)
        self.chatbox.pack()


        # Create the entry widget
        self.entry = customtkinter.CTkEntry(self.frame, placeholder_text="type something", width=350)
        self.entry.pack(side=tk.LEFT, padx=5)

        # Bind the entry widget to the "Return" key to send messages
        self.entry.bind("<Return>", self.send_message)

        # Create the send button
        self.send_button = customtkinter.CTkButton(self.frame, text="Enter", command=self.send_message, width=2)
        self.send_button.pack(side=tk.LEFT)

        # Pack the frame
        self.frame.pack(pady=10)

        # Set the focus to the entry widget
        self.entry.focus()   
        
    def waitmsg(self):
            message = "Disabling account in all platforms..."
            self.chatbox.insert(tk.END, "", "you_tag")
            self.chatbox.insert(tk.END, "Captain: " + message + "\n", "Captain_tag")  # Add the message to the chatbox
            self.chatbox.insert(tk.END, "\n", "you_tag")  # Add an empty line to the chatbox
            self.chatbox.see(tk.END)  # Scroll to the end of the chatbox
    
    def show_weather(self):
        message = "What is the weather like in Houston?"
        self.entry.delete(0, tk.END)
        self.entry.insert(0, message)
        self.send_message()
        
    def youtube_summarize(self):
        message = "Type in a link from youtube and I will summarize it!"
        self.generate_summary(message) # add this line to generate summary
        self.chatbox.config(state=tk.NORMAL)  # Set the chatbox state to normal
        self.chatbox.insert(tk.END, "Captain: ", "Captain_tag")  # Add the bot's name to the chatbox
        self.root.after(25, self.print_char, 0, message)  # Call the print_char function to print out the weather message''
        
    def ADChangePassword(self):
        
        # Check if message is in the correct form
        
        if ADChange:
            # Extract user name and new password from message
            user_upn = ADChange.group(1)
            new_password = ADChange.group(2)
            print(new_password)
                # Construct query for user details
        elif ADChange2:
            user_upn = ADChange2.group(1)
            new_password = ADChange2.group(2)
            print(new_password)
        
        
        tenant_id = 'ab4f77ee-0f8c-41e0-835d-a71d8ef869dc'
        client_id = '7e07fc1b-4825-46e0-9c36-d9029057e0c9'
        client_secret = '7rw8Q~UKK6uosMEz1lwVWanIcvWV-auTtlQtubNu'

            # Microsoft Graph API endpoints
        base_url = 'https://graph.microsoft.com/v1.0'
        users_url = f'{base_url}/users' 

            # Authentication 
        authority_url = f'https://login.microsoftonline.com/{tenant_id}'
        app = msal.ConfidentialClientApplication(client_id, authority=authority_url, client_credential=client_secret)

        result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
        headers = {
            'Authorization': 'Bearer ' + result['access_token'],
            'Content-Type': 'application/json'
            }

            # Get user details
        user_query = f"displayName eq '{user_upn}'"
        user_response = requests.get(f"{users_url}?$filter={user_query}", headers=headers)
        
        if user_response.ok:
            
            users_data = user_response.json()['value']
            
            if len(users_data) > 0:
                    user_data = user_response.json()['value'][0]
                    user_url = f"{users_url}/{user_data['id']}"
                    
                    # Update user's password
                    password_payload = {
                        "passwordProfile": {
                            "forceChangePasswordNextSignIn": False,
                        "password": new_password 
                        }
                    }
                    password_response = requests.patch(user_url, headers=headers, data=json.dumps(password_payload))
                                    
                    if password_response.ok:
                        message = f"Password updated to {new_password} for user '{user_upn}'"
                        self.chatbox.config(state=tk.NORMAL)
                        self.chatbox.insert(tk.END, "Captain: ", "Captain_tag")
                        self.root.after(25, self.print_char, 0, message)
                    else:
                        message = f"Failed to update password for user '{user_upn}': {password_response.text}"
                        self.chatbox.config(state=tk.NORMAL)
                        self.chatbox.insert(tk.END, "Captain: ", "Captain_tag")
                        self.root.after(25, self.print_char, 0, message)
            else: 
                    message = f"Failed to find user '{user_upn}'"
                    self.chatbox.config(state=tk.NORMAL)
                    self.chatbox.insert(tk.END, "Captain: ", "Captain_tag")
                    self.root.after(25, self.print_char, 0, message)
                    
    def ADDisable(self):
            # Check if message is in the correct format
            if ADDisable:
                self.waitmsg()
                self.entry.configure(state=tk.DISABLED)  # Disable the entry widget
                self.send_button.configure(state=tk.DISABLED)  # Disable the send button
                # Extract user name 
                user_upn = ADDisable.group(1)
                
            elif ADDisable2:
                self.waitmsg()
                self.entry.configure(state=tk.DISABLED)  # Disable the entry widget
                self.send_button.configure(state=tk.DISABLED)  # Disable the send button
                user_upn = ADDisable2.group(1)
                
            

            # Extract user name and new password from message
            user_query = f"displayName eq '{user_upn}'"
            
            tenant_id = 'ab4f77ee-0f8c-41e0-835d-a71d8ef869dc'
            client_id = '7e07fc1b-4825-46e0-9c36-d9029057e0c9'
            client_secret = '7rw8Q~UKK6uosMEz1lwVWanIcvWV-auTtlQtubNu'

                # Microsoft Graph API endpoints
            base_url = 'https://graph.microsoft.com/v1.0'
            users_url = f'{base_url}/users'
            # Ask for 

                # Authentication 
            authority_url = f'https://login.microsoftonline.com/{tenant_id}'
            app = msal.ConfidentialClientApplication(client_id, authority=authority_url, client_credential=client_secret)

            result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
            headers = {
                'Authorization': 'Bearer ' + result['access_token'],
                'Content-Type': 'application/json'
                }

                # Get user details
            user_query = f"displayName eq '{user_upn}'"
            user_response = requests.get(f"{users_url}?$filter={user_query}", headers=headers)
            

            # Get user details
            user_response = requests.get(f"{users_url}?$filter={user_query}", headers=headers)
            if user_response.ok:
                users_data = user_response.json()['value']
                if len(users_data) > 0:
                    user_data = users_data[0]
                    user_url = f"{users_url}/{user_data['id']}"
                    # Disable user
                    user_payload = {
                        "accountEnabled": False
                    }
                    user_response = requests.patch(user_url, headers=headers, data=json.dumps(user_payload))
                    if user_response.ok:

                        messageout = f"User '{user_upn}' is disabled"
                        
                        self.chatbox.config(state=tk.NORMAL)
                        self.chatbox.insert(tk.END, "Captain: ", "Captain_tag")
                        self.root.after(25, self.print_char, 0, messageout)
                    else:
                        message = f"Failed to disable user '{user_upn}': {user_response.text}"
                        
                        self.chatbox.config(state=tk.NORMAL)
                        self.chatbox.insert(tk.END, "Captain: ", "Captain_tag")
                        self.root.after(25, self.print_char, 0, message)
                else:
                    message = f"Failed to find user '{user_upn}'"
                    self.chatbox.config(state=tk.NORMAL)
                    self.chatbox.insert(tk.END, "Captain: ", "Captain_tag")
                    self.root.after(25, self.print_char, 0, message)
            else:
                message = f"Error: {user_response.text}"
                self.chatbox.config(state=tk.NORMAL)  
                self.chatbox.insert(tk.END, "Captian: ", "Captain_tag") 
                self.root.after(25, self.print_char, 0, message)
        
    def generate_summary(self, message):
        openai.api_key = ""
        youtubelink = "https://www.youtube.com/watch?v="

        if message.startswith(youtubelink):
            think = "watching video..."
            self.entry.delete(0, tk.END)
            self.print_char(0, think)  # Call the print_char function to print out the summary
            
            videosSearch = VideosSearch(f"{message}", limit = 1)

            results = videosSearch.result()

            for video in results['result']:
                print(video['id'])

            try:
                transcript = YouTubeTranscriptApi.get_transcript(video['id'])
                transcript_text = " ".join([line['text'] for line in transcript])
                formatter = TextFormatter()
                txt_formatted = formatter.format_transcript(transcript)

                with open('transcript.txt', 'w', encoding='utf-8') as txt_file:
                    txt_file.write(txt_formatted)

                chunk_size = 3500
                chunks = [transcript_text[i:i+chunk_size] for i in range(0, len(transcript_text), chunk_size)]

                summary_ = ""
                for chunk in chunks:
                    summary_ += chunk
                    
                print(summary_)
                    
                messages = [{"role": "system", "content": f"You are a chatbot created by saul.Your name is Captain. You will summarize the following text from a youtube video: {summary_}"},]
                message__ = message
                if message__:
                    messages.append({"role": "user", "content": message},)
                    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                    reply = chat.choices[0].message.content
                    messages.append({"role": "assistant", "content": reply})
                    self.summary = reply

                # Update the chatbox with the summary
                self.chatbox.delete("end-2c", tk.END)  # Delete the last character of the chatbox (i.e. the ellipsis)
                self.chatbox.insert(tk.END, "", "Captain_tag")
                self.chatbox.insert(tk.END, "\n\nCaptain: ", "Captain_tag")  # Add the bot's name to the chatbox
                self.print_char(0, reply)  # Call the print_char function to print out the summary
                self.chatbox.see(tk.END)  # Scroll to the end of the chatbox
                

            except TranscriptsDisabled:
                print(f"Transcripts are disabled for video ID.")

        # Enable the entry widget and the send button
        self.entry.configure(state=tk.NORMAL)
        self.send_button.configure(state=tk.NORMAL)
       
    def get_weather(self, city):
        api_key = "b57e3ef2ca4ff9b71795ba74f612f99f"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            message = f"The weather in {city} is currently {weather_description} with a temperature of {temperature} degrees Fahrenheit."
            if "rain" in weather_description or "storm" in weather_description or "shower" in weather_description:
                message += " It looks like it might rain today."
            else:
                message += " It doesn't look like it will rain today."
            self.entry.configure(state=tk.DISABLED)  # Disable the entry widget
            self.send_button.configure(state=tk.DISABLED)  # Disable the send button
            self.chatbox.delete("end-2c", tk.END)  # Delete the last character of the chatbox (i.e. the ellipsis)
            self.chatbox.insert(tk.END, "", "Captain_tag")
            self.chatbox.insert(tk.END, "\n\nCaptain: ", "Captain_tag")  # Add the bot's name to the chatbox
            self.root.after(25, self.print_char, 0, message)  # Call the print_char function to print out the weather message
            self.chatbox.see(tk.END)  # Scroll to the end of the chatbox
        else:
            error_message = f"Sorry, I could not retrieve weather information for {city}."
            self.chatbox.insert(tk.END, "", "Captain_tag")
            self.chatbox.insert(tk.END, "\nCaptain: " + error_message, "Captain_tag")  # Add the error message to the chatbox
            self.chatbox.insert(tk.END, "\n\n", "Captain_tag")  # Add a newline character to the chatbox
            self.chatbox.see(tk.END)  # Scroll to the end of the chatbox
            self.entry.configure(state=tk.NORMAL)  # Enable the entry widget
            self.send_button.configure(state=tk.NORMAL)  # Enable the send button
            self.entry.focus()  # Set the focus to the entry widget
            
    def print_char(self, *args):
        index = args[0]
        message = args[1]
        if index < len(message):
            self.chatbox.insert(tk.END, message[index], "Captain_tag")  # Add the next character to the chatbox
            self.chatbox.see(tk.END)  # Scroll to the end of the chatbox
            self.root.after(25, self.print_char, index+1, message)  # Call the function again after a delay of 25ms
        elif index == len(message):
            self.chatbox.insert(tk.END, "\n\n", "Captain_tag")  # Add a newline character to the chatbox
            self.entry.configure(state=tk.NORMAL)  # Enable the entry widget
            self.send_button.configure(state=tk.NORMAL)  # Enable the send button
            self.entry.focus()  # Set the focus to the entry widget



    def send_message(self, event=None):
        youtubelink = "https://www.youtube.com/watch?v="
        message = self.entry.get()  # Get the message from the entry widget
        self.entry.delete(0, tk.END)  # Clear the entry widget
        self.chatbox.config(state=tk.NORMAL)  # Set the chatbox state to normal
        self.chatbox.insert(tk.END, "", "you_tag")
        self.chatbox.insert(tk.END, "You: " + message + "\n", "you_tag")  # Add the message to the chatbox
        self.chatbox.insert(tk.END, "\n", "you_tag")  # Add an empty line to the chatbox
        self.chatbox.see(tk.END)  # Scroll to the end of the chatbox
        
        global match
        global ADChange
        global ADDisable
        global ADDisable2
        global ADChange2
        
        Weather = re.match(r"What is the weather like in (?P<city>.+)\?", message, re.IGNORECASE)
        ADChange =  re.match(r"Change\s+(.*?)'s\s+password\s+to\s+(.*)", message, re.IGNORECASE)
        ADChange2 =  re.match(r"Change\s+(.*?)\s+password\s+to\s+(.*)", message, re.IGNORECASE)
        ADDisable =  re.match(r"Disable\s+(.*?)'s\s+account", message, re.IGNORECASE)
        ADDisable2 =  re.match(r"Disable\s+(.*?)\s+account", message, re.IGNORECASE)
               
        if Weather:
        # Extract the city name from the message
            city = Weather.group("city")

        # Call the get_weather method with the city name as an argument
            self.get_weather(city)
        
        elif ADChange or ADChange2:
            self.ADChangePassword()
            
        elif ADDisable or ADDisable2:
            self.ADDisable()
            
        elif message.startswith(youtubelink):
            # Disable the entry widget and the send button while the bot is processing the response
            self.entry.configure(state=tk.DISABLED)
            self.send_button.configure(state=tk.DISABLED)

            # Create a new thread to generate the summary in the background
            t = threading.Thread(target=self.generate_summary, args=(message,))
            t.start()

            
        else:
            
        # Update the chatbox after 500ms to display the bot's response
            self.root.after(500, self.get_response, message)

            # Disable the entry widget and the send button while the bot is processing the response
            self.entry.configure(state=tk.DISABLED)
            self.send_button.configure(state=tk.DISABLED)

    def get_response(self, message):
        
        messages = [{"role": "system", "content": "You are a chatbot created by Saul.You go by the name of Captain. Captain works for a company called Inchcape Shipping Services and your purpose is to aid the IT department. The IT Department uses a Hybryd environment for O365. What the serivce desk analysts primarly deal with is 8x8, Outlook, Printers, Security Issues via threatspike, our ticketing system is ZOHO Desk"},]
        if message:
            messages.append({"role": "user", "content": message},)
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            message = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": message})
        
        # message_ = f"You are a chatbot made by Saul, you will respond to the following message:{message}"
        # response_ = openai.Completion.create(engine="text-davinci-003", prompt=message_, max_tokens=650)
        # response = response_.choices[0].text.strip()

        # Remove the last message from the chatbox and add the bot's response
        self.chatbox.delete("end-1c", tk.END)  # Delete the last character of the chatbox (i.e. the newline character)
        self.chatbox.insert(tk.END, "\nCaptain: ", "Captain_tag")  # Add the bot's name to the chatbox
        self.root.after(25, self.print_char, 0, message)  # Call the print_char function to print out the weather message''
        

        
                    

if __name__ == '__main__':
    root = customtkinter.CTk()
    root.title("Inchcape Bot")
    chatbot = ChatBot(root)
    root.mainloop()