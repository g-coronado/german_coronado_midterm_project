#from unittest import case
import subprocess
from datetime import date
from db import db_load_players, db_move_player, list_of_players, VALID_POSITIONS, db_remove_player, db_add_player, db_edit_player_position, db_edit_player_stats

today_date = date.today()
empty_space = ' '
dash_space = '-'
equal_space = '='

def display_valid_positions():
     positions = ''
     counter = 1
     for p in VALID_POSITIONS:
        if counter < len(VALID_POSITIONS):
            positions += f'{p}, '
            counter += 1
        else:
            positions += f'{p}'
            counter += 1
     return(positions)


def game_information():
    game_list = []
    subprocess.run('cls', shell=True)
    print(f'Welcome to the Baseball Team Manager!')
    print(f'Please enter the date of the next game to get started.')
    
    game_year = input(f'\nEnter the year of the next game: ')
    while not game_year.isdigit():
        print(f'Invalid input. Please enter a valid year for the game.')
        game_year = input(f'\nEnter the year of the next game: ')
    game_list.append(int(game_year))
    
    game_month = input(f'\nEnter the month of the next game: ')
    while not game_month.isdigit() or int(game_month) < 1 or int(game_month) > 12:
        print(f'Invalid input. Please enter a valid month for the next game between 1 and 12.')
        game_month = input(f'\nEnter the month of the next game: ')
    game_list.append(int(game_month))
    
    game_day = input(f'\nEnter the day of the next game: ')
    while not game_day.isdigit() or int(game_day) < 1 or int(game_day) > 31:
        print(f'Invalid input. Please enter a valid day for the next game between 1 and 31.')
        game_day = input(f'\nEnter the day of the next game: ') 
    game_list.append(int(game_day))
    
    days_until_game = (date(int(game_year), int(game_month), int(game_day)) - today_date).days
    if days_until_game < 0:
        game_list.append(' ')
    else:
        game_list.append(days_until_game)
    return game_list

def display_main_menu(next_game_list):
        subprocess.run('cls', shell=True)
        print(equal_space*64)
        print(f'\n                    Baseball Team Manager')
        print(f'CURRENT DATE:{empty_space*5}{today_date.strftime("%Y-%m-%d")}')
        print(f'GAME DATE:{empty_space*8}{(next_game_list[0])}-{(next_game_list[1]):02d}-{(next_game_list[2]):02d}')
        print(f'DAYS UNTIL GAME:{empty_space*2}{next_game_list[3]}')
        print(f'\nMENU OPTIONS')
        print('1 - Display lineup')
        print('2 - Add player')
        print('3 - Remove player')
        print('4 - Move player')
        print('5 - Edit player Position')
        print('6 - Edit player stats')
        print('7 - Exit program')
        print(f'\nPOSITIONS')
        print(display_valid_positions())
        print(equal_space*64)
        return input(f'\nMenu option: ')


def display_lineup():
    print (f'\n{empty_space*8}Player{empty_space*16}POS{empty_space*5}AB{empty_space*7}H{empty_space*6}AVG')
    print (dash_space*64)
    try:
        
        for player_info in list_of_players:
            print(f'{player_info[0]:<7} {player_info[1]:<21} {player_info[2]:<7} {player_info[3]:<8} {player_info[4]:<6} {player_info[5]:<6}')
    except:
        print("Error loading player data from file. Please check the file locationa and structure and try again.")


def exit_program():
    print('Goodbye!')


def remove_player():
    print(f'These are the players in the team: \n')
    display_lineup()
    player_to_delete = input('Enter the user to be removed: ')
    print(db_remove_player(player_to_delete)) 


def add_player():
    name = input('Enter the name of the player to add: ')
    position = input('Enter the position of the player to add: ')
    while position not in VALID_POSITIONS:
        print(f'Invalid position. Please enter a valid position from the following list: {display_valid_positions()}')
        position = input('Enter the position of the player to add: ')   
    
    at_bat = input('Enter the number of at-bats for the player to add: ')
    while not at_bat.isdigit():
        print('Invalid input. Please enter a valid number for at-bats.')
        at_bat = input('Enter the number of "At bats" for the player to add: ')
    if int(at_bat) == 0:
        print('Setting at-bats to 0 sets automatically hits to 0 for this player.')
        hits = '0'
    else:
        hits = input('Enter the number of "Hits" for the player to add: ')
    while not hits.isdigit():
        print('Invalid input. Please enter a valid number for hits.')
        hits = input('Enter the number of hits for the player to add: ') 
    while int(hits) > int(at_bat):
        print(f'Hits cannot be greater than at-bats. Please enter a number less than or equal to {at_bat}.')
        hits = input('Enter the number of hits for the player to add: ')   
    result = db_add_player(name, position, at_bat, hits)
    print(result)


def edit_player_position():
    length_of_list = len(list_of_players)
    while True:
        lineup_number_to_edit = input('Lineup number to edit: ')
        if lineup_number_to_edit.isdigit() and 1 <= int(lineup_number_to_edit) <= length_of_list:
            break
        else:
            print(f'Invalid input. Please enter a valid lineup number between 1 and {length_of_list}.')
    lineup_number_to_edit = int(lineup_number_to_edit)
    print(f'{list_of_players[lineup_number_to_edit - 1][1]} has been selected.')
    new_position = input('New position: ')
    while new_position not in VALID_POSITIONS:
        print(f'Invalid position. Please enter a valid position from the following list: {display_valid_positions()}')
        new_position = input('New position: ')
    result = db_edit_player_position(lineup_number_to_edit, new_position)
    print(result)
 
   
def edit_player_stats():
    length_of_list = len(list_of_players)
    while True:
        lineup_number_to_edit = input('Lineup number to edit: ')
        if lineup_number_to_edit.isdigit() and 1 <= int(lineup_number_to_edit) <= length_of_list:
            break
        else:
            print(f'Invalid input. Please enter a valid lineup number between 1 and {length_of_list}.')
    lineup_number_to_edit = int(lineup_number_to_edit)
    print(f'{list_of_players[lineup_number_to_edit - 1][1]} has been selected.')
    new_ab = input('New At Bat statistics: ')
    while not new_ab.isdigit():
        print('Invalid input. Please enter a valid number for at-bats.')
        new_ab = input('New At Bat statistics: ')
    if int(new_ab) == 0:
        print('Setting at-bats to 0 sets automatically hits to 0 for this player.')
        new_hits = '0'
    else:
        new_hits = input('New Hits statistics: ')
    while not new_hits.isdigit():
        print('Invalid input. Please enter a valid number for hits.')
        new_hits = input('New Hits statistics: ')
    while int(new_hits) > int(new_ab):
        print(f'Hits cannot be greater than at-bats. Please enter a number less than or equal to {new_ab}.')
        new_hits = input('New Hits statistics: ')   
    result = db_edit_player_stats(lineup_number_to_edit, new_ab, new_hits)
    print(result)


def move_player():
    length_of_list = len(list_of_players)
    while True:
        lineup_number_to_move = input('Lineup number to move: ')
        if lineup_number_to_move.isdigit() and 1 <= int(lineup_number_to_move) <= length_of_list:
            break
        else:
            print(f'Invalid input. Please enter a valid lineup number between 1 and {length_of_list}.')
    lineup_number_to_move = int(lineup_number_to_move)
    print(f'{list_of_players[lineup_number_to_move - 1][1]} has been selected.')
    while True:
        new_lineup_number = input('Enter the new Lineup number: ')
        if new_lineup_number.isdigit() and 1 <= int(new_lineup_number) <= length_of_list:
            break
        else:
            print(f'Invalid input. Please enter a valid lineup number between 1 and {length_of_list}.')
    new_lineup_number = int(new_lineup_number)
    result = db_move_player(lineup_number_to_move, new_lineup_number)
    print(result)


def main():
    db_load_players()
    #next_game_information()
    user_choice = display_main_menu(game_information())
    while True:
        match user_choice:
            case '1':
                display_lineup()
                user_choice = input(f'\nMenu option: ')
            case '2':
                add_player()
                user_choice = input(f'\nMenu option: ')
            case '3':
                remove_player()
                user_choice = input(f'\nMenu option: ')
            case '4':
                move_player()
                user_choice = input(f'\nMenu option: ')
            case '5':
                edit_player_position()
                user_choice = input(f'\nMenu option: ')
            case '6':
                edit_player_stats()
                user_choice = input(f'\nMenu option: ')
            case '7':
                exit_program()
                break
            case _:
                print("That is an invalid option. Please try again and select a valid option from the menu.")
                user_choice = display_main_menu()


if __name__ == "__main__":
    main()