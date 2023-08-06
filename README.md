# Pywiki-Lite
* Username: https://www.twitch.tv/
* ClientID/Client Secret: https://dev.twitch.tv/
* Bot Oauth Token: https://twitchapps.com/tmi/ (Just the token, no "oauth:")
* Channel: Whatever you want, only one.
* OpenAI API Key: https://platform.openai.com/ 
<br /><br />
Tags for Context:
* \<name> : Same as Username
* \<channel> : Same as Channel
* \<game> : The current game from the twitch API
* \<author> : The chatter that sent the prompt
* \<emotes> : A CSV of all global twitch emotes (Uses a lot of tokens, remove this tag to save on openai credit)
* \<UTC>" : Raw UTC date and time output
* \<chatter_pronouns> : The pronouns of the chatter that sent the prompt
* \<streamer_pronouns> : The pronouns of the streamer
* \<users> : A CSV of the users in chat (Pulled from irc, may take time to update, large lists can use a lot of tokens, so you may not want to use this tag)
<br /><br />
Features:
* Pronouns from https://pronouns.alejo.io/
* Previous and next rocket launch from https://thespacedevs.com/
* Auto-reply frequency slider (% per message)
* GPT model (Features are available currently in 0613 builds, if you don't have access to gpt-4 please set it to one of the gpt-3-turbo options)
<br /><br />

![Screenshot 2023-08-06 075105.png](..%2F..%2F..%2FOneDrive%2FPictures%2FScreenshots%2FScreenshot%202023-08-06%20075105.png)