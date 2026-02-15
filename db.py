import pandas as pd
from pathlib import Path

def load_players():
    FILENAME = Path(__file__).parent /"players.csv"
    # FILENAME = Path(__file__).parent /"player.csv"
    return pd.read_csv(FILENAME)

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



