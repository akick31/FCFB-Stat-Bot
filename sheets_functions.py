import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from util import *

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('FCFBRollCallBot-2d263a255851.json', scope)
gc = gspread.authorize(credentials)


sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1bGhm3g5g2jMGUgJCh0rfAxTU8iNw_Jxd85CEFUiXbJM/edit?usp=sharing')
all_teams = sh.worksheet("All Time WL")

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)


"""
Update every single team
"""


async def update_all_teams(client):
    team_column = all_teams.col_values(3)

    # Remove blank and "Team" cell
    team_column.pop(0)
    team_column.pop(0)

    for team in team_column:
        num_seasons = int(config_data['num_seasons'])
        for i in range(1, num_seasons + 1):
            season_num = str(i)
            await search_season_scores(client, team, season_num)


