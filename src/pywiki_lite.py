#!/usr/bin/python
import os
import ctypes
import json
import queue
import sys
import threading
import time

import configparser
import random
import re
import traceback

import irc.bot
import requests

import openai
from datetime import datetime, timezone
if sys.platform.startswith('win'):
    from tkinter import messagebox, ttk
    import tkinter.scrolledtext as tkscrolled
    import tkinter as tk
from irc.dict import IRCDict
import argparse


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_version():
    return "1.11"  # Version Number


class TwitchBotGUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("pyWiki Lite")
        self.geometry("825x420")
        self.iconbitmap(default=resource_path('icon.ico'))

        # Make the window non-resizable
        self.resizable(False, False)

        # Variables for Twitch Bot configuration
        self.username = tk.StringVar()
        self.client_id = tk.StringVar()
        self.client_secret = tk.StringVar()
        self.bot_token = tk.StringVar()
        self.channel = tk.StringVar()
        self.openai_api_key = tk.StringVar()
        self.openai_api_model = tk.StringVar()

        # Variable to keep track of the bot state
        self.bot_running = False

        self.openai_models = ['gpt-4-0613', 'gpt-4', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo']

        self.create_widgets()

        # Load configuration from the INI file
        if not os.path.exists('config.ini'):
            self.save_configuration()
        self.load_configuration()

        # Bind the on_exit function to the closing event of the Tkinter window
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Initialize a Queue for handling log messages
        self.log_queue = queue.Queue()

        # Start a separate thread to update the log asynchronously
        self.log_thread = threading.Thread(target=self.process_log_queue)
        self.log_thread.daemon = True
        self.log_thread.start()

    # Function to handle selection change
    def on_selection_change(self, event):
        self.openai_api_model.set(self.openai_model_entry.get())
        print(self.openai_model_entry.get() + ' set')
        self.append_to_log(self.openai_model_entry.get() + ' set')

    def show_about_popup(self):
        about_text = "pyWiki Lite " + get_version() + "\n©2023 Ixitxachitl\nAnd ChatGPT"
        messagebox.showinfo("About", about_text)

    def append_to_log(self, message):
        self.log_queue.put(message)

    def process_log_queue(self):
        while True:
            try:
                message = self.log_queue.get_nowait()
                self.log_text.config(state=tk.NORMAL)  # Enable the Text widget for editing
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)  # Scroll to the bottom of the text widget
                self.log_text.config(state=tk.DISABLED)  # Disable the Text widget for editing
            except queue.Empty:
                pass
            time.sleep(.1)

    def toggle_stay_on_top(self):
        if self.attributes("-topmost"):
            self.attributes("-topmost", False)
            self.stay_on_top_button.config(relief="raised")
        else:
            self.attributes("-topmost", True)
            self.stay_on_top_button.config(relief="sunken")

    def create_widgets(self):
        # Set the column weight to make text inputs expand horizontally
        self.columnconfigure(1, weight=1)

        tk.Label(self, text="pyWiki Lite Configuration", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2,
                                                                                      pady=10, padx=10, sticky='w')
        tk.Label(self, text="Context", font=("Helvetica", 16)).grid(row=0, column=3, columnspan=1,
                                                                    pady=10, padx=(0, 10), sticky='w')

        # Twitch Bot Username Entry
        tk.Label(self, text="Username:").grid(row=1, column=0, padx=(10, 5), sticky="e")
        self.bot_username_entry = tk.Entry(self, textvariable=self.username)
        self.bot_username_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(2, 0))

        # ClientID Entry
        tk.Label(self, text="ClientID:").grid(row=2, column=0, padx=(10, 5), sticky="e")
        self.client_id_entry = tk.Entry(self, show="*", textvariable=self.client_id)
        self.client_id_entry.grid(row=2, column=1, sticky="ew", padx=(0, 10))

        # Client Secret Entry
        tk.Label(self, text="Client Secret:").grid(row=3, column=0, padx=(10, 5), sticky="e")
        self.client_secret_entry = tk.Entry(self, show="*", textvariable=self.client_secret)
        self.client_secret_entry.grid(row=3, column=1, sticky="ew", padx=(0, 10))

        # Twitch Bot Token Entry
        tk.Label(self, text="Bot OAuth Token:").grid(row=4, column=0, padx=(10, 5), sticky="e")
        self.bot_token_entry = tk.Entry(self, show="*", textvariable=self.bot_token)
        self.bot_token_entry.grid(row=4, column=1, sticky="ew", padx=(0, 10))

        # Channel Entry
        tk.Label(self, text="Channel:").grid(row=5, column=0, padx=(10, 5), sticky="e")
        self.channel_entry = tk.Entry(self, textvariable=self.channel)
        self.channel_entry.grid(row=5, column=1, sticky="ew", padx=(0, 10))

        # OpenAI API Key Entry
        tk.Label(self, text="OpenAI API Key:").grid(row=6, column=0, padx=(10, 5), sticky="e")
        self.openai_api_key_entry = tk.Entry(self, show="*", textvariable=self.openai_api_key)
        self.openai_api_key_entry.grid(row=6, column=1, sticky="ew", padx=(0, 10))

        # OpenAI Model
        self.openai_model_entry = ttk.Combobox(self, textvariable=self.openai_api_model, state="readonly")
        self.openai_model_entry['values'] = self.openai_models
        self.openai_model_entry.grid(row=0, column=4, sticky="e", padx=10)

        # Set the default value for the dropdown box
        self.openai_model_entry.current(0)

        # Bind the event handler to the selection change event
        self.openai_model_entry.bind('<<ComboboxSelected>>', self.on_selection_change)

        self.stay_on_top_button = tk.Button(self, text="📌", command=self.toggle_stay_on_top)
        self.stay_on_top_button.grid(row=0, column=5, sticky="e", padx=10)

        self.about_button = tk.Button(self, text="ℹ️", command=self.show_about_popup, borderwidth=0)
        self.about_button.grid(row=0, column=6, sticky="e", padx=10)

        # Create a slider widget
        self.frequency_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.frequency_slider.grid(row=7, column=0, columnspan=2, padx=10, pady=2, sticky="ew")

        # Start/Stop Bot Button
        self.bot_toggle_button = tk.Button(self, text="Start Bot", command=self.toggle_bot, anchor='e',
                                           justify='center')
        self.bot_toggle_button.grid(row=0, column=1, columnspan=1, sticky="e", pady=10, padx=10)

        # Create a Text widget to display bot messages
        self.log_text = tkscrolled.ScrolledText(self, wrap="word", height=11, state=tk.DISABLED)
        self.log_text.grid(row=8, column=0, columnspan=2, padx=10, pady=(3, 0), sticky="w", )

        # Create a Text widget to display the input string
        self.input_text = tkscrolled.ScrolledText(self, wrap="word", height=22, width=40, undo=True,
                                                  autoseparators=True, maxundo=-1)
        self.input_text.grid(row=1, column=3, columnspan=4, rowspan=9, padx=(0, 10), pady=2, sticky="ne")

    def write_to_text_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"Successfully wrote to {file_path}")
        except Exception as e:
            print(f"Error occurred while writing to {file_path}: {e}")

    def load_configuration(self):
        config = configparser.ConfigParser()
        if not config.read('config.ini'):
            return

        if 'TwitchBot' in config:
            section = config['TwitchBot']
            self.username.set(section.get('username', ''))
            self.client_id.set(section.get('ClientID', ''))
            self.client_secret.set(section.get('ClientSecret', ''))
            self.bot_token.set(section.get('BotOAuthToken', ''))
            self.channel.set(section.get('InitialChannels', ''))
            self.openai_api_key.set(section.get('OpenAIAPIKey', ''))
            if not section.get('InputString', ''):
                self.input_text.insert(tk.END, "You are a twitch chatbot, your username is <name> and your pronouns "
                                               "are They/Them. The name of the streamer is <channel> and their "
                                               "pronouns are <streamer_pronouns>. The streamer is playing <game>. The "
                                               "name of the chatter is <author> and their pronouns are "
                                               "<chatter_pronouns>. The current date and time are: <UTC>. Global "
                                               "twitch emotes that you can use are <emotes>.")
            else:
                self.input_text.insert(tk.END, section.get('InputString', ''))

            if not section.get('Model', ''):
                self.openai_api_model.set('gpt-4-0613')
            else:
                self.openai_api_model.set(section.get('Model', ''))

            if not section.get('Frequency', ''):
                self.frequency_slider.set(0)
            else:
                self.frequency_slider.set(section.get('Frequency', ''))

    def save_configuration(self):
        config = configparser.ConfigParser()
        config['TwitchBot'] = {
            'username': self.username.get(),
            'ClientID': self.client_id.get(),
            'ClientSecret': self.client_secret.get(),
            'BotOAuthToken': self.bot_token.get(),
            'InitialChannels': self.channel.get(),
            'OpenAIAPIKey': self.openai_api_key.get(),
            'InputString': self.input_text.get('1.0', 'end'),
            'Model': self.openai_api_model.get(),
            'Frequency': self.frequency_slider.get(),
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def start_bot(self):
        if not self.bot_running:
            self.bot_running = True
            self.bot_toggle_button.config(text="Stop Bot")

            # Start the bot in a separate thread
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=False)
            self.bot_thread.start()
            return

    def run_bot(self):
        # This method will be executed in a separate thread
        # Create and run the bot here
        self.bot = TwitchBot(self.username.get(), self.client_id.get(), self.client_secret.get(), self.bot_token.get(),
                             self.channel.get(), self.openai_api_key.get())
        self.bot.start()
        return

    def stop_bot(self):
        if self.bot_running:
            self.bot_running = False
            self.bot_toggle_button.config(text="Start Bot")
            self.write_to_text_file("log.txt", self.log_text.get("1.0", tk.END).strip())
            if hasattr(self, "bot"):
                self.bot.connection.quit()
                self.bot.disconnect()
                # self.bot.die()
                # self.bot_thread.join()
                self.terminate_thread(self.bot_thread)
                print("Stopped")
                self.append_to_log("Stopped")

    def terminate_thread(self, thread):
        """Terminates a python thread from another thread.

        :param thread: a threading.Thread instance
        """
        if not thread.is_alive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def on_exit(self):
        self.save_configuration()
        self.stop_bot()
        self.destroy()

    def toggle_bot(self):
        self.save_configuration()
        if self.bot_running:
            self.bot_toggle_button.config(relief="raised")
            self.bot_username_entry.config(state="normal")
            self.client_id_entry.config(state="normal")
            self.client_secret_entry.config(state="normal")
            self.bot_token_entry.config(state="normal")
            self.channel_entry.config(state="normal")
            self.openai_api_key_entry.config(state="normal")
            self.stop_bot()
        else:
            self.bot_toggle_button.config(relief="sunken")
            self.bot_username_entry.config(state="disabled")
            self.client_id_entry.config(state="disabled")
            self.client_secret_entry.config(state="disabled")
            self.bot_token_entry.config(state="disabled")
            self.channel_entry.config(state="disabled")
            self.openai_api_key_entry.config(state="disabled")
            self.start_bot()


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, client_secret, token, channel, openai_api_key):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.channel = '#' + channel
        self.client_credentials = requests.post('https://id.twitch.tv/oauth2/token?client_id='
                                                + self.client_id
                                                + '&client_secret='
                                                + self.client_secret
                                                + '&grant_type=client_credentials'
                                                + '&scope=user%3amanage%3achat_color'
                                                + '').json()
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key
        self.pronoun_cache = {}

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/helix/users?login=' + channel
        headers = {'Authorization': 'Bearer ' + self.client_credentials['access_token'],
                   'Client-ID': self.client_id,
                   'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['data'][0]['id']

        # Get the user id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/helix/users?login=' + username
        headers = {'Authorization': 'Bearer ' + self.client_credentials['access_token'],
                   'Client-ID': self.client_id,
                   'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers).json()
        self.user_id = r['data'][0]['id']

        # Get list of global emotes
        url = 'https://api.twitch.tv/helix/chat/emotes/global'
        headers = {'Authorization': 'Bearer ' + self.client_credentials['access_token'],
                   'Client-ID': self.client_id,
                   'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers).json()
        self.emotes = []
        for emote in r['data']:
            self.emotes.append(emote['name'])

        self.functions = [
            {
                "name": "get_user_pronouns",
                "description": "Get the pronouns of a specified user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user": {
                            "type": "string",
                            "description": "The name of the person to look up pronouns for.",
                        },
                    },
                    "required": ["user"],
                },
            },
            {
                "name": "get_launch",
                "description": "Get the next or previous scheduled space launch",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "when": {
                            "type": "string",
                            "enum": ["next", "previous"]
                        },
                    },
                },
            },
        ]

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        app.append_to_log('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    def get_game(self):
        # Get the current game
        url = 'https://api.twitch.tv/helix/channels?broadcaster_id=' + self.channel_id
        headers = {'Authorization': 'Bearer ' + self.client_credentials['access_token'],
                   'Client-ID': self.client_id,
                   'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers).json()
        return r['data'][0]['game_name']

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)
        app.append_to_log('Joining ' + self.channel)
        self.connection = c

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def get_launch(self, when, **kwargs):
        if when == 'next':
            url = 'https://ll.thespacedevs.com/2.2.0/launch/upcoming/?mode=list'
        else:
            url = 'https://ll.thespacedevs.com/2.2.0/launch/previous/?mode=list'
        return json.dumps(requests.get(url).json()["results"][0])

    def get_pronouns(self, author, **kwargs):
        # Check if pronouns exist in the cache
        if author in self.pronoun_cache:
            return self.pronoun_cache[author]

        url = 'https://pronouns.alejo.io/api/users/' + author.lower()
        r = requests.get(url).json()

        pronoun_mapping = {
            'aeaer': 'Ae/Aer',
            'any': 'Any',
            'eem': 'E/Em',
            'faefaer': 'Fae/Faer',
            'hehim': 'He/Him',
            'heshe': 'He/She',
            'hethem': 'He/They',
            'itits': 'It/Its',
            'other': 'Other',
            'perper': 'Per/Per',
            'sheher': 'She/Her',
            'shethey': 'She/They',
            'theythem': 'They/Them',
            'vever': 'Ve/Ver',
            'xexem': 'Xe/Xem',
            'ziehir': 'Zie/Hir'
        }

        pronouns = r[0]['pronoun_id'] if r else 'unknown'
        pronoun = pronoun_mapping.get(pronouns, 'unknown')

        print('Got ' + author + ' pronouns ' + pronoun)
        app.append_to_log('Got ' + author + ' pronouns ' + pronoun)

        self.pronoun_cache[author] = pronoun

        return pronoun

    def parse_string(self, input_string, author, user_message):
        replacements = {
            "<name>": self.username,
            "<channel>": self.channel[1:],
            "<game>": self.get_game(),
            "<author>": author,
            "<emotes>": ','.join(map(str, self.emotes)),
            "<UTC>": str(datetime.now(timezone.utc)),
            "<chatter_pronouns>": self.get_pronouns(author),
            "<streamer_pronouns>": self.get_pronouns(self.channel[1:])
        }

        for placeholder, replacement in replacements.items():
            input_string = input_string.replace(placeholder, replacement)

        sentences = input_string.split('. ')
        parsed_list = [{"role": "system", "content": sentence} for sentence in sentences]
        parsed_list.append({"role": "user", "content": user_message})

        return parsed_list

    def _on_disconnect(self, c, e):
        self.channels = IRCDict()
        self.recon.run(self)
        print('Disconnected')
        app.append_to_log('Disconnected')

    def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        message = e.arguments[0]
        author = ''
        for tag in e.tags:
            if tag['key'] == 'display-name':
                author = tag['value']
                break
        print(author + ": " + message)
        app.append_to_log(author + ": " + message)

        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            app.append_to_log('Received command: ' + cmd)
            self.do_command(e, cmd)
        elif message.lower() == (self.username + " yes").lower() or message.lower() == \
                ('@' + self.username + " yes").lower():
            c.privmsg(self.channel, ":)")
            app.append_to_log(self.username + ': ' + ":)")
        elif message.lower() == (self.username + " no").lower() or message.lower() == \
                ('@' + self.username + " no").lower():
            c.privmsg(self.channel, ":(")
            app.append_to_log(self.username + ': ' + ":(")
        elif message.lower().startswith(("thanks " + self.username).lower()) or \
                message.lower().startswith(("thanks @" + self.username).lower()):
            c.privmsg(self.channel, "np")
            app.append_to_log(self.username + ': ' + "np")
        else:
            rand_chat = random.random()
            # print(str(round(rand_chat*100,3)) + ':' + str(app.frequency_slider.get()))
            if rand_chat <= float(app.frequency_slider.get()) / 100 or self.username.lower() in message.lower() or \
                    "@" + self.username.lower() in message.lower():
                self.input_text = app.input_text.get('1.0', 'end')
                retry = 0
                while retry < 3:
                    message_array = self.parse_string(self.input_text, author, message)
                    try:
                        response = openai.ChatCompletion.create(model=app.openai_api_model.get(),
                                                                messages=message_array,
                                                                functions=self.functions
                                                                )

                        response_message = response["choices"][0]["message"]

                        # Step 2: check if GPT wanted to call a function
                        if response_message.get("function_call"):
                            # Step 3: call the function
                            # Note: the JSON response may not always be valid; be sure to handle errors
                            available_functions = {
                                "get_user_pronouns": self.get_pronouns,
                                "get_launch": self.get_launch,
                            }  # only one function in this example, but you can have multiple
                            function_name = response_message["function_call"]["name"]
                            function_to_call = available_functions[function_name]
                            function_args = json.loads(response_message["function_call"]["arguments"])
                            function_response = function_to_call(
                                author=function_args.get("user"),
                                when=function_args.get("when"),
                            )

                            # Step 4: send the info on the function call and function response to GPT
                            message_array.append(response_message)  # extend conversation with assistant's reply
                            # noinspection PyTypeChecker
                            message_array.append(
                                {
                                    "role": "function",
                                    "name": function_name,
                                    "content": function_response,
                                }
                            )  # extend conversation with function response
                            response = openai.ChatCompletion.create(
                                model=app.openai_api_model.get(),
                                messages=message_array,
                            )  # get a new response from GPT where it can see the function response

                        if hasattr(response, 'choices'):
                            response.choices[0].message.content = \
                                response.choices[0].message.content.strip().replace('\r', ' ').replace('\n', ' ')
                            response.choices[0].message.content = ' '.join(
                                re.split(r'(?<=[.:;])\s', response.choices[0].message.content)[:3])
                            while response.choices[0].message.content.startswith('.') or response.choices[
                                0].message.content.startswith(
                                '/'):
                                response.choices[0].message.content = response.choices[0].message.content[1:]
                            if response.choices[0].message.content.lower().startswith(self.username.lower()):
                                response.choices[0].message.content = response.choices[0].message.content[
                                                                      len(self.username):]
                            c.privmsg(self.channel, response.choices[0].message.content[:500])
                            app.append_to_log(self.username + ': ' + response.choices[0].message.content[:500])
                            break
                        else:
                            print(response)
                            app.append_to_log(response)

                    except Exception as e:
                        retry += 1
                        print(str(e))
                        print(traceback.format_exc())
                        app.append_to_log(str(e))
                        app.append_to_log(traceback.format_exc())

    def do_command(self, e, cmd):
        c = self.connection


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyWiki Lite")
    parser.add_argument("--version", action="store_true", help="Show the version number")
    args = parser.parse_args()

    if args.version or not sys.platform.startswith('win'):
        print(get_version())
        sys.exit()

    app = TwitchBotGUI()
    app.mainloop()
