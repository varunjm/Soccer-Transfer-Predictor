import sys
import pickle

pkl_file = open('DT_classifier_data.pkl', 'rb')
player_field_pos = pickle.load(pkl_file)

def get_field_position(player_id):
    return player_field_pos[player_id]
