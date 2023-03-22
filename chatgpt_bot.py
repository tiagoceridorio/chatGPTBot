import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GPT_API_KEY = os.getenv('GPT_API_KEY')
GPT_API_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GPT_API_KEY}"
}


class ChatGPTBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!chatgpt'):
            prompt = message.content[9:].strip()
            response = self.generate_response(prompt)
            await message.channel.send(response)

    def generate_response(self, prompt):
        data = {
            "prompt": prompt,
            "max_tokens": 50,
            "temperature": 0.8,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        response = requests.post(GPT_API_URL, headers=headers, json=data)
        response_text = response.json()["choices"][0]["text"].strip()
        return response_text


client = ChatGPTBot()
client.run(TOKEN)
