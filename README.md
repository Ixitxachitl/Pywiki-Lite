# pyWiki Lite

pyWiki Lite is a chatbot application that interfaces with OpenAI, GPT-4-All, and Twitch. This guide will walk you through the process of obtaining a Twitch Client ID and Client Secret, setting up a redirect URI, and acquiring an OpenAI API key for use with pyWiki Lite.

## Twitch Client ID and Client Secret

1. **Create a Twitch Developer Account:**
   - If you don't have a Twitch developer account, sign up for one on the [Twitch Developer Portal](https://dev.twitch.tv/).

2. **Create a New Application:**
   - Log in to your Twitch Developer account.
   - Go to the [Applications](https://dev.twitch.tv/console/apps) section.
   - Click on the "Register Your Application" button.

3. **Fill Out Application Details:**
   - Provide a name for your application (e.g., "MyTwitchApp").
   - Set the OAuth Redirect URLs to `http://localhost:3000/`.
   - Choose an appropriate category for your application.
   - Agree to the terms of service and click the "Create" button.

4. **Obtain Client ID and Client Secret:**
   - After creating the application, you'll receive a **Client ID** and a **Client Secret**. Keep these secure, as they are required for authentication.

## OpenAI API Key

1. **Sign Up for an OpenAI Account:**
   - If you don't have an OpenAI account, sign up for one on the [OpenAI website](https://www.openai.com/).

2. **Generate an API Key:**
   - Log in to your OpenAI account.
   - Navigate to the API section of your account.

3. **Create a New API Key:**
   - Create a new API key and provide a descriptive name for it.

4. **Retrieve Your API Key:**
   - Once the API key is generated, it will be displayed. This key is necessary for making API requests to OpenAI.

Remember to keep your API keys secure and avoid sharing them publicly or hardcoding them directly into your code. Use best practices for managing sensitive information in your applications.

## Login
- Once you enter your **Client ID** and **Client Secret** you may click login to direct you to a browser login, log into the account that you want your bot to be.
- OpenAI API Key is necessary to generate responses, it is possible to use gpt4all instead of OpenAI without entering a key as long as the necessary files are in the same directory. (see below)

## Additional Resources

- [Twitch Developer Documentation](https://dev.twitch.tv/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## Tags for Context:
* \<name> : Same as Username
* \<channel> : Same as Channel
* \<game> : The current game from the twitch API
* \<author> : The chatter that sent the prompt
* \<emotes> : A CSV of all global twitch emotes (Uses a lot of tokens, remove this tag to save on openai credit)
* \<time> : Raw local date and time output (\<UTC> also works)
* \<chatter_pronouns> : The pronouns of the chatter that sent the prompt
* \<streamer_pronouns> : The pronouns of the streamer
* \<users> : A CSV of the users in chat (Pulled from irc, may take time to update, large lists can use a lot of tokens, so you may not want to use this tag. If ignore is checked the bot sees the list as unknown.)

## Features:
* Pronouns from https://pronouns.alejo.io/
* Previous and next rocket launch from https://thespacedevs.com/
* Auto-reply frequency slider (% per message, set to 0 to completely mute as the mute button only mutes responses to the bots name.)
* GPT model (If you don't have access to gpt-4 please set it to one of the gpt-3-turbo options)
* Will get a list of users in chat if requested without using the tag. (Unless the ignore box is checked)
* Double click user to see account creation date
* Offline chat generation using gpt4all, place https://gpt4all.io/models/ggml-mpt-7b-chat.bin or https://gpt4all.io/models/wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin in the same directory as the script/app
<br /><br />

![image](https://github.com/Ixitxachitl/Pywiki-Lite/assets/16951681/66bae59d-eab1-4342-a894-bc659ef05a52)

[<img width="100" src="https://uploads-ssl.webflow.com/5c14e387dab576fe667689cf/6494083ae7c39da6541f3c3e_TextLogo_white_stroke%402x-p-500.png">](https://ko-fi.com/pywiki/)
