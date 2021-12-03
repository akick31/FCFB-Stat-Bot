import discord
import json
from sheets_functions import *

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

"""
Login to Discord and run the bot

"""


def login_discord():
    token = config_data['discord_token']

    client = discord.Client()

    @client.event
    async def on_message(message):
        msg = message.content.lower()
        if msg.startswith('$start'):
            await message.channel.send("Updating teams in the stat sheet")
            await update_all_teams(client)

    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token)