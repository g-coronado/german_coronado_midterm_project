import pandas as pd
from pathlib import Path
import os

VALID_POSITIONS = ('C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P')
list_of_players = []
FILENAME = Path(__file__).parent /"players.csv"


def db_load_players():
    players = pd.read_csv(FILENAME, header=None)
    number_of_rows = players.shape[0]
    number_of_columns = players.shape[1]
    for row in range(number_of_rows):
        player = []
        player.append(row+1)
        for column in range(number_of_columns):
            real_value = players.iloc[row, column]
            if hasattr(real_value, 'item'):
                real_value = real_value.item()
            player.append(real_value)
        average = average_calculator(player[4], player[3])
        player.append(average)
        list_of_players.append(player)


def db_add_player(name, position, at_bat, hits):
    average = average_calculator(hits, at_bat)
    new_player = [len(list_of_players) + 1, name, position, at_bat, hits, average]
    try:
        list_of_players.append(new_player)
        update_file()
        message = f'Player {name} has been added to the team.'
    except:
        message = f"Error adding player {name} to the team. Please check the file location and structure and try again."
    return message


def db_remove_player(player_to_delete):
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


def db_move_player(lineup_number_to_move, new_lineup_number):
    player_to_move = list_of_players.pop(lineup_number_to_move - 1)
    list_of_players.insert(new_lineup_number - 1, player_to_move)
    number_of_rows = len(list_of_players)
    for i in range(number_of_rows):
        list_of_players[i][0] = i + 1
    update_file()
    return f'{player_to_move[1]} has been moved to lineup position {new_lineup_number}.'
    

def db_edit_player_position(lineup_number_to_edit, new_position):
    try:
        list_of_players[lineup_number_to_edit - 1][2] = new_position
        update_file()
        message = f'{list_of_players[lineup_number_to_edit - 1][1]} has been updated to position {new_position}.'
    except:
        message = f"Error updating player position. Please check the file location and structure and try again."
    return message


def db_edit_player_stats(lineup_number_to_edit, new_ab, new_hits):
    try:
        average = average_calculator(new_hits, new_ab)
        list_of_players[lineup_number_to_edit - 1][3] = new_ab
        list_of_players[lineup_number_to_edit - 1][4] = new_hits
        list_of_players[lineup_number_to_edit - 1][5] = average
        update_file()
        message = f'{list_of_players[lineup_number_to_edit - 1][1]} has been updated with new stats.'
    except:
        message = f"Error updating player stats. Please check the file location and structure and try again."
    return message


def update_file():
    to_update = pd.DataFrame(list_of_players, columns=["index", "player_name", "position", "at_bat", "hits", "average"])
    to_update = to_update.drop(columns=["index", "average"])   # remove index column    
    to_update.to_csv(FILENAME, index=False, header=False)


def average_calculator(hits, at_bat):
    try:
        average = format(round(int(hits) / int(at_bat), 3),"0.3f")
    except ZeroDivisionError:
        average = "0.000"
    return average



