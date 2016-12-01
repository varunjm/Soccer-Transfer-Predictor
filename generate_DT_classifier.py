import sqlite3
import pandas as pd
import sys
import pickle

database = './database.sqlite'
conn = sqlite3.connect(database)
cur = conn.cursor()
player_field_pos = {}

result = cur.execute("SELECT DISTINCT P.player_api_id, pxy.x, pxy.y from Player_xy pxy, Player P, Player_Attributes pa WHERE P.player_api_id = pxy.id and pa.player_api_id = P.player_api_id and P.birthday < \'1995-01-01 00:00:00\' and pa.date > \'2012-06-30\';")

for player in result:
    x = player[1]
    y = player[2]
    if y == 1:                  # Goal Keeper
        player_class = 1
    elif y > 1 and y < 5:       # Defense
        player_class = 3
    elif y >= 5 and y <= 6:     # Defensive-mid
        player_class = 3
    elif y == 7:
        if x >= 4 and x <= 6:   # Defensive-mid
            player_class = 3
        elif x == 7:            # Midfielder
            player_class = 2
        else:                   # Attacking-mid
            player_class = 2
    elif y >= 8 and y <= 9:     # Attacking-mid
        player_class = 2
    elif y >= 10:
        if x < 4 or x >= 7:     # Attacking-mid
            player_class = 2
        else:                   # Attack
            player_class = 0

    player_field_pos[player[0]] = player_class

output = open('DT_classifier_data.pkl', 'wb')
pickle.dump(player_field_pos, output)
output.close()
