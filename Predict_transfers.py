import DT_classifier
from scipy.spatial import distance
import sys
import heapq
import pickle

players = {}
team_skills = {}

#   0 : attack
#   1 : goal-keepers
#   2 : midfield
#   3 : defense

skill_count = {
    0: 13,
    1: 1,
    2: 8,
    3: 11
}

def process_all_players():
    global team_skills
    global players

    pkl_file = open('player_teams_data.pkl', 'rb')
    team_skills = pickle.load(pkl_file)
    players =  pickle.load(pkl_file)
    pkl_file.close()

def sum_matrix(tuple_list):
    total = 0
    for tuple in tuple_list:
        total += sum(tuple[1])
    return total

def get_weak_player(season, team):
    current_team_skills = team_skills[season][team]
    team_attack_count = len(current_team_skills[0]) * skill_count[0]
    team_defense_count = len(current_team_skills[3]) * skill_count[3]
    team_midfield_count = len(current_team_skills[2]) * skill_count[2]

    team_attack = sum_matrix(current_team_skills[0]) / team_attack_count
    team_defense =  sum_matrix(current_team_skills[3]) / team_defense_count
    team_midfield =  sum_matrix(current_team_skills[2]) / team_midfield_count

    if team_attack > team_midfield:
        min_field = 2
        min = team_midfield
    else:
        min_field = 0
        min = team_attack

    if team_defense < min:
        min_field = 3

    min_stat = 100
    min_player = -1
    for tuple in current_team_skills[min_field]:
        if len(tuple[1]) == 0:
            continue
        avg = sum(tuple[1])/len(tuple[1])
        if min_stat > avg:
            min_stat = avg
            min_player = tuple[0]

    # print (str(team) + " : " +str(min_player)+" : "+str(team_attack)+" : "+str(team_midfield)+" : "+str(team_defense) )
    return (min_player, min_field)

def avg(skill_list):
    l = len(skill_list)
    return sum(skill_list)/l

def player_in_team(season, team, field_pos, min_player):
    for player in team_skills[season][team][field_pos]:
        if player[0] == min_player:
            return True
    return False

def main():
    process_all_players()
    found = ['Replacement found', 'Replacement not found']
    for season in [2013, 2014]:
        transfer_match_count = 0
        weakplayer_match_count = 0
        print('Season: '+str(season))
        for team in team_skills[season]:
            min_player, min_field = get_weak_player(season, team)
            weakplayer_match_count += 1
            text = ''
            sum = None
            count = 0
            for player in team_skills[season][team][min_field]:
                if len(player[1]) == 0:
                    continue
                if player[0] != min_player:
                    count += 1
                    if sum == None:
                        sum = player[1]
                    else:
                        sum = [x + y for x, y in zip(sum, player[1])]

            players_count = count
            if count != 0:
                team_avg_skill = [x / players_count for x in sum]
            else:
                team_avg_skill = [75] * skill_count[min_field]

            min = sys.maxint
            min_player
            dist_list = []
            count = 0
            if len(team_avg_skill) == 0:
                team_avg_skill = [75] * skill_count[min_field]

            for player in players[season]:
                count += 1
                if min_field == players[season][player][0] and len(players[season][player][1]) != 0 and players[season][player][2] != team:
                    # dist = distance.euclidean(team_avg_skill,players[season][player][1])
                    dist = abs(avg(team_avg_skill) - avg(players[season][player][1]))
                    heapq.heappush(dist_list, (dist, player, players[season][player][2]))
            number_of_matches = 80 #len(dist_list)

            flag = 1
            for i in range(number_of_matches):
                result = heapq.heappop(dist_list)
                if player_in_team(season+1, team, min_field, result[1]):
                    transfer_match_count += 1
                    flag = 0
                    break

            print("Team: "+str(team),"Weak Player: "+str(min_player), found[flag])
        print("Total predictions correct: " + str(transfer_match_count) + '/' + str(weakplayer_match_count))
main()
