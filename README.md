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
* *Pronouns from https://pronouns.alejo.io/
* *Previous and next rocket launch from https://thespacedevs.com/
* Auto-reply frequency slider (% per message)
* GPT model (*Features are available currently in 0613 builds, if you don't have access to gpt-4 please set it to one of the gpt-3-turbo options)
* Will get a list of users in chat if requested without using the tag. (Excluding the bot and the streamer unless the ignore box is checked)
* Double click user to see account creation date
<br /><br />

![image](https://github.com/Ixitxachitl/Pywiki-Lite/assets/16951681/66bae59d-eab1-4342-a894-bc659ef05a52)

[<img width="100px" src="https://github.com/Ixitxachitl/Pywiki-Lite/assets/16951681/0bee033e-56d1-4126-9432-c613920de7db" />][Ko-fi](https://ko-fi.com/pywiki/)
