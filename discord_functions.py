import discord
import json
from sheets_functions import *

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

with open('team_info.json', 'r') as config_file:
    team_info_data = json.load(config_file)

"""
Login to Discord and run the bot

"""


def login_discord():
    token = config_data['discord_token']

    client = discord.Client()

    @client.event
    async def on_message(message):
        message = message.content.lower()
        if message.startswith('$start'):
            update_all_teams()

    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token)


"""
Search through season scores channel and count up information
"""

def search_season_scores(team, season_num):
