import pandas as pd
from pathlib import Path

VALID_POSITIONS = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P']
list_of_players = []

def load_players():
    FILENAME = Path(__file__).parent /"players.csv"
    # FILENAME = Path(__file__).parent /"player.csv"
    players = pd.read_csv(FILENAME)
    number_of_rows = players.shape[0]
    number_of_columns = players.shape[1]

    for row in range(number_of_rows):
        player = []
        player.append(row + 1)
        for column in range(number_of_columns):
            real_value = players.iloc[row, column]
            if hasattr(real_value, 'item'):
                real_value = real_value.item()
            player.append(real_value)
        list_of_players.append(player)
    # return list_of_players

def add_player():
    print('Add player option')

def remove_player():
    print("Delete player option")

def move_player():
    print("Move player option")

def edit_player_position():
    print("Edit player position option")

def edit_player_status():
    print("Edit player status option")

#print(load_players())  # delete after testing
# print (len(VALID_POSITIONS ))


