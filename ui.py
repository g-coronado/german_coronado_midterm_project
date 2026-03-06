
import subprocess
import db

from datetime import date
from objects import Player
from db import (
    db_load_players, db_add_player, db_remove_player, db_move_player,
    db_edit_player_position, db_edit_player_stats, VALID_POSITIONS
    )

today_date = date.today()
empty_space = ' '
dash_space = '-'
equal_space = '='
lineup = None


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

    subprocess.run('cls', shell=True)
    print('Welcome to the Baseball Team Manager!')
    print('Please enter the date of the next game.\n')
    game_year = input(f'\nEnter the year of the game: ')
    
    if game_year.strip() != '':

        while not game_year.isdigit():
            print(f'Invalid input. Please enter a valid year for the game.')
            game_year = input(f'\nEnter the year of the game: ')

        game_month = input(f'\nEnter the month of the game: ')
        while not game_month.isdigit() or int(game_month) < 1 or int(game_month) > 12:
            print(f'Invalid input. Please enter a valid month for the game between 1 and 12.')
            game_month = input(f'\nEnter the month of the game: ')

        game_day = input(f'\nEnter the day of the game: ')
        while not game_day.isdigit() or int(game_day) < 1 or int(game_day) > 31:
            print(f'Invalid input. Please enter a valid day for the game between 1 and 31.')
            game_day = input(f'\nEnter the day of the game: ') 
    
        days_until_game = (date(int(game_year), int(game_month), int(game_day)) - today_date).days
        
        if days_until_game < 0: 
            return [int(game_year), int(game_month), int(game_day), ' ']
        else:
            return [int(game_year), int(game_month), int(game_day), days_until_game]
        
    else:
        return [' ', ' ', ' ', ' ']


def display_main_menu(game_list):
    if game_list[0] == ' ':
        game_date_str = ' '
    else:
        game_date_str = f'{game_list[0]}-{game_list[1]:02d}-{game_list[2]:02d}'
        
    subprocess.run('cls', shell=True)
    print(equal_space* 64)
    print(f'{empty_space * 20}Baseball Team Manager\n')
    print(f'CURRENT DATE:{empty_space*5}{today_date}')
    print(f'GAME DATE:{empty_space*8}{game_date_str}')
    print(f'DAYS UNTIL GAME:{empty_space*2}{game_list[3]}')
    print(f'\nMENU OPTIONS')
    print('1 - Display lineup')
    print('2 - Add player')
    print('3 - Remove player')
    print('4 - Move player')
    print('5 - Edit player position')
    print('6 - Edit player stats')
    print('7 - Exit program')
    print(f'\nPOSITIONS')
    print(display_valid_positions())
    print(equal_space * 64)
    return input(f'\nMenu option: ')


def display_lineup():
    print(f'\n{empty_space * 4}Player{empty_space * 15}POS{empty_space * 3}AB{empty_space * 4}H{empty_space * 5}AVG')
    print(dash_space* 64)

    for i, p in enumerate(lineup, start=1):
        print(f'{i:<3} {p.player_full_name:<20} {p.position:<5} {p.at_bats:<5} {p.hits:<5} {p.batting_average:<5}')


def collect_player_stats():
    new_ab = input('New At Bat statistics: ')
    
    while not new_ab.isdigit():
        print('Invalid input. Please enter a valid number for at-bats.')
        new_ab = input('New At Bat statistics: ')
    
    if int(new_ab) == 0:
        print('Setting at-bats to 0 sets automatically hits to 0 for this player.')
        return 0, 0

    while True:
        new_hits = input('New Hits statistics: ')
        
        if not new_hits.isdigit():
            print('Invalid input. Please enter a valid number for hits.')
            continue
        
        if int(new_hits) > int(new_ab):
            print(f'Hits cannot be greater than at-bats. Please enter a number less than or equal to {new_ab}.')
            continue
        break  
    return int(new_ab), int(new_hits)


def collect_player_position(origin_function):
    if origin_function == 'add_player':
        message = 'Enter the position of the player to add: '
    elif origin_function == 'edit_player_position':
        message = 'New position: ' 

    player_position = input(message)
    while player_position not in VALID_POSITIONS:
        print(f'Invalid position. Please enter a valid position from the following list: {display_valid_positions()}')
        player_position = input('New position: ')
    
    return player_position
    

def check_valid_lineup_number(origin_function):
    length_of_list = lineup.number_of_players
    
    if origin_function == 'edit_player_stats':
        message = 'Lineup number to edit: '
        display_lineup()
    
    elif origin_function == 'delete_player':
        message = 'Lineup number to remove: '
        display_lineup()
    
    elif origin_function == 'edit_player_position':
        message = 'Lineup number to edit: '
        display_lineup()
    
    elif origin_function == 'move_player':
        message = 'Lineup number to move: '
        display_lineup()
    
    elif origin_function == 'move_player_new':
        message = 'New lineup number: '
    
    while True:
        lineup_number_to_edit = input(f'\n{message} ')
        
        if lineup_number_to_edit.isdigit() and 1 <= int(lineup_number_to_edit) <= length_of_list:
            break
        else:
            print(f'Invalid input. Please enter a valid lineup number between 1 and {length_of_list}.')
    return int(lineup_number_to_edit)


def add_player():
    first_name = input(f'Enter player\'s first name: ')
    last_name = input(f'Enter player\'s last name: ')
    position = collect_player_position('add_player')
    at_bats, hits = collect_player_stats()
    player = Player(first_name, last_name, position, at_bats, hits)
    db_add_player(lineup, player)
    print(f'{player.player_full_name} added.')


def remove_player():
    player_to_delete = check_valid_lineup_number('delete_player') - 1
    player = db_remove_player(lineup, player_to_delete)
    print(f'{player.player_full_name} removed.')


def move_player():  
    lineup_number_to_move = check_valid_lineup_number('move_player') - 1
    new_lineup_number = check_valid_lineup_number('move_player_new') - 1
    player = db_move_player(lineup, lineup_number_to_move, new_lineup_number)
    print(f'{player.player_full_name} moved to position {new_lineup_number+1}.')    


def edit_player_position():
    display_lineup()
    lineup_number_to_edit = check_valid_lineup_number('edit_player_position')
    new_pos = collect_player_position('edit_player_position')
    player = db_edit_player_position(lineup, lineup_number_to_edit, new_pos)
    print(f'{player.player_full_name} updated to {new_pos}.')


def edit_player_stats():
    lineup_number_to_edit = check_valid_lineup_number('edit_player_stats')   
    player = lineup.retrieve_player(lineup_number_to_edit)
    print(f'{player.player_full_name} has been selected.')
    new_ab, new_hits = collect_player_stats()
    player = db_edit_player_stats(lineup, int(lineup_number_to_edit)-1, int(new_ab), int(new_hits))
    print(f'{player.player_full_name} stats updated.')


def exit_program():
    print('Goodbye!')


def main():
    db.connect()
    global lineup
    lineup = db_load_players()
    user_choice = display_main_menu(game_information())

    while True:
        match user_choice:
            case '1':
                try:
                    display_lineup()
                except:
                    print('Error loading player data. Please check the file location and structure, and try again.')
                    exit_program()
                    break
            case '2':
                add_player()  
            case '3':
                remove_player()

            case '4':
                move_player()   
            case '5':
                edit_player_position()              
            case '6':
                edit_player_stats()    
            case '7':
                exit_program()
                break
            case _:
                print("That is an invalid option. Please try again and select a valid option from the menu.")

        user_choice = input(f'\nMenu option: ')


if __name__ == "__main__":
    main()