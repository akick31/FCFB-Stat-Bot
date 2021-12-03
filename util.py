import discord
import json

with open('team_info.json', 'r') as config_file:
    team_info_data = json.load(config_file)

with open('channel_info.json', 'r') as config_file:
    channel_info_data = json.load(config_file)

"""
Search through season scores channel and count up information
"""


async def search_season_scores(client, team, season_num):
    lower_team = team.lower()
    channel_id = channel_info_data[season_num]
    channel = client.get_channel(int(channel_id))
    messages = await channel.history(oldest_first=True, limit=1000).flatten()

    print("START OF " + team.upper() + " SEARCH FOR SEASON " + season_num + "\n")
    for msg in messages:
        all_time_wins = int(team_info_data[team]["all_time_wins"])
        all_time_losses = int(team_info_data[team]["all_time_losses"])
        ranked_wins = int(team_info_data[team]["ranked_wins"])
        ranked_losses = int(team_info_data[team]["ranked_losses"])
        conference_wins = int(team_info_data[team]["conference_wins"])
        conference_losses = int(team_info_data[team]["conference_losses"])
        ccg_wins = int(team_info_data[team]["ccg_wins"])
        ccg_losses = int(team_info_data[team]["ccg_losses"])
        bowl_wins = int(team_info_data[team]["bowl_wins"])
        bowl_losses = int(team_info_data[team]["bowl_losses"])
        playoff_app = int(team_info_data[team]["playoff_app"])
        playoff_wins = int(team_info_data[team]["playoff_wins"])
        playoff_losses = int(team_info_data[team]["playoff_losses"])
        championships = int(team_info_data[team]["championships"])
        weeks_ranked = int(team_info_data[team]["weeks_ranked"])
        highest_rank = int(team_info_data[team]["highest_rank"])

        msg = msg.content.lower()

        if "defeats" in msg:
            winning_team = msg.split('defeats')[0]

            # Handle ULM edge case
            if "louisiana-monroe" in msg.split('defeats')[1]:
                losing_team = "louisiana-monroe"
                other_info = msg.split('louisiana-monroe')[1].split("-")[1]
            elif "-" in msg:
                losing_team = msg.split('defeats')[1].split("-")[0].rsplit(' ', 1)[0]
                other_info = msg.split('defeats')[1].split("-")[1]
            # Handle "64 to 21" edge case
            elif "to" in msg:
                losing_team = msg.split('defeats')[1].split("to")[0].rsplit(' ', 1)[0]
                other_info = msg.split('defeats')[1].split("to")[1]

        else:
            winning_team = None
            losing_team = None

        if winning_team is not None and "#" in winning_team:
            winning_team_compare = winning_team.split("#")[1].split(' ', 1)[1]
        else:
            winning_team_compare = winning_team

        if losing_team is not None and "#" in losing_team:
            losing_team_compare = losing_team.split("#")[1].split(' ', 1)[1]
        else:
            losing_team_compare = losing_team

        if lower_team == winning_team_compare or lower_team == losing_team_compare:
            # If team won
            if lower_team in winning_team_compare:
                all_time_wins = all_time_wins + 1
                team_info_data[team]["all_time_wins"] = str(all_time_wins)

                # Determine if team was ranked
                if "#" in winning_team:
                    rank = int(winning_team.split('#')[1].split(' ')[0])
                    weeks_ranked = weeks_ranked + 1
                    team_info_data[team]["weeks_ranked"] = str(weeks_ranked)
                    if rank < highest_rank:
                        team_info_data[team]["highest_rank"] = str(rank)

                # If won against ranked opponent
                if "#" in losing_team:
                    ranked_wins = ranked_wins + 1
                    team_info_data[team]["ranked_wins"] = str(ranked_wins)

                # If won conference championship
                if "championship" in msg and "win the national championship" not in msg:
                    ccg_wins = ccg_wins + 1
                    team_info_data[team]["ccg_wins"] = str(ccg_wins)

                # If won a bowl game
                if "bowl" in other_info:
                    bowl_wins = bowl_wins + 1
                    team_info_data[team]["bowl_wins"] = str(bowl_wins)

                # If won a playoff game
                if "cfp" in other_info or "playoff" in other_info:
                    playoff_app = playoff_app + 1
                    team_info_data[team]["playoff_app"] = str(playoff_app)
                    playoff_wins = playoff_wins + 1
                    team_info_data[team]["playoff_wins"] = str(playoff_wins)
                    if "win the national championship" in msg:
                        championships = championships + 1
                        team_info_data[team]["championships"] = str(championships)

            # If team lost
            if lower_team in losing_team_compare:
                all_time_losses = all_time_losses + 1
                team_info_data[team]["all_time_losses"] = str(all_time_losses)

                # Determine if team was ranked
                if "#" in losing_team:
                    rank = int(winning_team.split('#')[1].split(' ')[0])
                    weeks_ranked = weeks_ranked + 1
                    team_info_data[team]["weeks_ranked"] = str(weeks_ranked)
                    if rank < highest_rank:
                        team_info_data[team]["highest_rank"] = str(rank)

                # If lost against ranked opponent
                if "#" in winning_team:
                    ranked_losses = ranked_losses + 1
                    team_info_data[team]["ranked_wins"] = str(ranked_losses)

                # If lost conference championship
                if "championship" in msg and "win the national championship" not in msg:
                    ccg_losses = ccg_losses + 1
                    team_info_data[team]["ccg_losses"] = str(ccg_losses)

                # If lost a bowl game
                if "bowl" in other_info:
                    bowl_losses = bowl_losses + 1
                    team_info_data[team]["bowl_losses"] = str(bowl_losses)

                # If lost a playoff game
                if "cfp" in other_info or "playoff" in other_info:
                    playoff_app = playoff_app + 1
                    team_info_data[team]["playoff_app"] = str(playoff_app)
                    playoff_losses = playoff_losses + 1
                    team_info_data[team]["playoff_losses"] = str(playoff_losses)

    print("END OF " + team.upper() + " SEARCH FOR SEASON " + season_num + "\n\n")