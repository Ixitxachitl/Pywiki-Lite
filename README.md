# Pywiki-Lite
* Username: Login (Redirect URI is 'http://localhost:3000')
* ClientID/Client Secret: https://dev.twitch.tv/
* Channel: Whatever you want, only one.
* OpenAI API Key: https://platform.openai.com/ 
<br /><br />
Tags for Context:
* \<name> : Same as Username
* \<channel> : Same as Channel
* \<game> : The current game from the twitch API
* \<author> : The chatter that sent the prompt
* \<emotes> : A CSV of all global twitch emotes (Uses a lot of tokens, remove this tag to save on openai credit)
* \<time> : Raw local date and time output (\<UTC> also works)
* \<chatter_pronouns> : The pronouns of the chatter that sent the prompt
* \<streamer_pronouns> : The pronouns of the streamer
* \<users> : A CSV of the users in chat (Pulled from irc, may take time to update, large lists can use a lot of tokens, so you may not want to use this tag)
<br /><br />
Features:
* Pronouns from https://pronouns.alejo.io/
* Previous and next rocket launch from https://thespacedevs.com/
* Auto-reply frequency slider (% per message)
* GPT model (If you don't have access to gpt-4 please set it to one of the gpt-3-turbo options)
* Will get a list of users in chat if requested without using the tag. (Excluding the bot and the streamer unless the ignore box is checked)
* Double click user to see account creation date
* Offline chat generation using gpt4all, place https://gpt4all.io/models/ggml-mpt-7b-chat.bin in the same directory as the script/app
<br /><br />

![image](https://github.com/Ixitxachitl/Pywiki-Lite/assets/16951681/66bae59d-eab1-4342-a894-bc659ef05a52)

[<img width="100" src="https://uploads-ssl.webflow.com/5c14e387dab576fe667689cf/6494083ae7c39da6541f3c3e_TextLogo_white_stroke%402x-p-500.png">](https://ko-fi.com/pywiki/)
