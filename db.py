import pandas as pd
from pathlib import Path
import os

VALID_POSITIONS = ('C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P')
list_of_players = []
list_of_players_dictionary = []
FILENAME = Path(__file__).parent /"players.csv"


def db_load_players_old():
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


def db_load_players():
    players = pd.read_csv(FILENAME, header=None)

    for row in range(players.shape[0]):
        name = players.iloc[row, 0]
        position = players.iloc[row, 1]
        at_bat = players.iloc[row, 2]
        hits = players.iloc[row, 3]

        if hasattr(at_bat, "item"):
            at_bat = at_bat.item()
        if hasattr(hits, "item"):
            hits = hits.item()

        average = average_calculator(hits, at_bat)
        player = {
            "lineup": row + 1,
            "name": name,
            "position": position,
            "at_bat": at_bat,
            "hits": hits,
            "average": average
        }
        list_of_players.append(player)


def db_add_player(name, position, at_bat, hits):
    average = average_calculator(hits, at_bat)
    new_player = {
        "lineup": len(list_of_players) + 1,
        "name": name,
        "position": position,
        "at_bat": at_bat,
        "hits": hits,
        "average": average
    }

    try:
        list_of_players.append(new_player)
        update_file()
        message = f'Player {name} has been added to the team.'
    except:
        message = f'Error adding player {name} to the team. Please check the file location and structure and try again.'
    
    return message


def db_remove_player(player_to_delete):
    try:
        name_of_player_to_delete = list_of_players[int(player_to_delete) - 1]['name']
        list_of_players.pop(int(player_to_delete) - 1)
        elements_in_list = len(list_of_players)
        for i in range(elements_in_list):
            list_of_players[i]['lineup'] = i + 1
        update_file()
        message = f'Player {name_of_player_to_delete} has been removed from the team.'
    except:
        message = f'Error removing player {name_of_player_to_delete} from the team. Please check the file location and structure and try again.'
    return message


def db_move_player(lineup_number_to_move, new_lineup_number):
    player_to_move = list_of_players.pop(lineup_number_to_move - 1)
    list_of_players.insert(new_lineup_number - 1, player_to_move)
    number_of_rows = len(list_of_players)
    
    for i in range(number_of_rows):
        list_of_players[i]['lineup'] = i + 1
    update_file()
    
    return f'{player_to_move['name']} has been moved to lineup position {new_lineup_number}.'
    

def db_edit_player_position(lineup_number_to_edit, new_position):
    try:
        list_of_players[lineup_number_to_edit - 1]['position'] = new_position
        update_file()
        message = f'{list_of_players[lineup_number_to_edit - 1]['name']} has been updated to position {new_position}.'
    except:
        message = f'Error updating player position. Please check the file location and structure and try again.'
    return message


def db_edit_player_stats(lineup_number_to_edit, new_ab, new_hits):
    try:
        average = average_calculator(new_hits, new_ab)
        list_of_players[lineup_number_to_edit - 1]['at_bat'] = new_ab
        list_of_players[lineup_number_to_edit - 1]['hits'] = new_hits
        list_of_players[lineup_number_to_edit - 1]['average'] = average
        update_file()
        message = f'{list_of_players[lineup_number_to_edit - 1]['name']} has been updated with new stats.'
    except:
        message = f'Error updating player stats. Please check the file location and structure and try again.'
    return message


def update_file():
    to_update = pd.DataFrame(list_of_players)
    to_update = to_update[["name", "position", "at_bat", "hits"]]    
    to_update.to_csv(FILENAME, index=False, header=False)


def average_calculator(hits, at_bat):
    try:
        average = format(round(int(hits) / int(at_bat), 3),"0.3f")
    except ZeroDivisionError:
        average = "0.000"
    return average


#db_load_players_to_list_of_dictionary() #delete after testing
#print(list_of_players_dictionary)  # delete after testing

