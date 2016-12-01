import sqlite3
import sys
import pickle
import DT_classifier

player_skills = {
    0: 'finishing, dribbling, volleys, heading_accuracy, strength, acceleration, sprint_speed, positioning, ball_control, short_passing, shot_power, reactions, agility',
    1: 'finishing',
    2: 'vision, ball_control, short_passing, long_passing, long_shots, penalties, dribbling, crossing',
    3: 'marking, standing_tackle, sliding_tackle, short_passing,long_passing, jumping, stamina, strength,aggression, interceptions, positioning'
}

skill_count = {
    0: 13,
    1: 1,
    2: 8,
    3: 11
}

database = './database.sqlite'
conn = sqlite3.connect(database)
cur = conn.cursor()
team_skills = {}
players = {}

def get_field_position(player_id):
        return DT_classifier.get_field_position(player_id)

def get_player_stats(player_id, field_pos, season):
    # print('get_player_stats')
    start_date = '(\'' + str(season) + '-07-01\')'
    end_date = '(\'' + str(season+1) + '-06-30\')'
    result = cur.execute( "Select " + player_skills[field_pos] + " from Player_Attributes where player_api_id =" + str(player_id) + "  and date between " + start_date + " and " + end_date + " order by date desc LIMIT 1;")
    player_stat_avg = 0
    player_stat = []

    for row in result:
        for skill in row:
            player_stat_avg += int(skill)
            player_stat.append(skill)

    player_stat_avg /= skill_count[field_pos]
    return player_stat_avg, player_stat

def process_all_players():
    teams = []
    result = cur.execute("SELECT DISTINCT team_api_id from PlayerTeamMod")
    for team in result:
        teams.append(team[0])

    for season in [2013, 2014, 2015]:
        team_skills[season] = {}
        players[season] = {}
        for team in teams:
            players_list = []
            team_skills[season][team] = {
                0: [],
                1: [],
                2: [],
                3: []
            }
            result = cur.execute("SELECT DISTINCT PT.player_api_id from PlayerTeamMod PT, Player P, Player_Attributes pa WHERE pa.player_api_id = P.player_api_id and P.player_api_id = PT.player_api_id AND PT.team_api_id = " + str(team) + " AND PT.season = \'" + str(season) + "/" + str(season+1) +"\' AND P.birthday < \'" + str(season-21)+ "-01-01 00:00:00\' and pa.date > \'2012-06-30\' order by PT.team_api_id")
            for player in result:
                players_list.append(player[0])

            for player in players_list:
                field_pos = get_field_position(player)
                player_stat_avg, player_stats = get_player_stats(player, field_pos, season)
                team_skills[season][team][field_pos].append((player, player_stats))
                players[season][player] = (field_pos, player_stats, team)

process_all_players()
pkl_file = open('player_teams_data.pkl', 'wb')
pickle.dump(team_skills, pkl_file, -1)
pickle.dump(players, pkl_file, -1)
pkl_file.close()
