import pandas as pd
from pathlib import Path

VALID_POSITIONS = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P']
list_of_players = []
FILENAME = Path(__file__).parent /"players.csv"

def load_players():
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


def to_add_player(name, position, at_bat, hits):
    average = round(int(hits) / int(at_bat), 3)
    new_player = [len(list_of_players) + 1, name, position, at_bat, hits, average]
    try:
        list_of_players.append(new_player)
        update_file()
        message = f'Player {name} has been added to the team.'
    except:
        message = f"Error adding player {name} to the team. Please check the file location and structure and try again."
    return message

def remove_player_from_database(player_to_delete):
    try:
        list_of_players.pop(int(player_to_delete) - 1)
        elements_in_list = len(list_of_players)
        for i in range(elements_in_list):
            list_of_players[i][0] = i + 1
        update_file()
        message = f'Player {player_to_delete} has been removed from the team.'
    except:
        message = f"Error removing player {player_to_delete} from the team. Please check the file location and structure and try again."
    return message

def move_player():
    print("Move player option, on db.py")

def edit_player_position():
    print("Edit player position option, on db.py")

def edit_player_status():
    print("Edit player status option, on db.py")

def update_file():
    to_update = pd.DataFrame(list_of_players, columns=["index", "player_name", "position", "at_bat", "hits", "average"])
    to_update = to_update.drop(columns=["index"])   # remove index column    
    to_update.to_csv(FILENAME, index=False)


# print(load_players())  # delete after testing
# print (len(VALID_POSITIONS ))


