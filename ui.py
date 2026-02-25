from db import list_of_players, VALID_POSITIONS, db_remove_player, db_add_player, db_edit_player_position, db_edit_player_stats

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

# Function to display the main menu
def display_main_menu():
        print('======================================================================')
        print(f'\n                    Baseball Team Manager')
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
        print('======================================================================')
        user_choice = select_option()
        # user_choice = input('Please select an option: ')
        return user_choice

# Function to prompt the user to select an option from the menu
def select_option():
    return input(f'\nMenu option: ')

# Function to display the lineup
def display_lineup():
    try:
        # display_players = load_players()
        print ('        Player                POS     AB       H      AVG')
        print ('----------------------------------------------------------------------')
        for player_info in list_of_players:
            print(f'{player_info[0]:<7} {player_info[1]:<21} {player_info[2]:<7} {player_info[3]:<8} {player_info[4]:<6} {player_info[5]:<6}')
               

    except:
        print("Error loading player data from file. Please check the file locationa and structure and try again.")

# Function to display the exit message      
def exit_program():
    print('Goodbye!')

def remove_player():
    print(f'These are the players in the team: \n')
    display_lineup()
    player_to_delete = input('Enter the user to be removed: ')
    result =db_remove_player(player_to_delete)
    #print(f'Player {player_to_delete} has been removed from the team.')
    print(result) 

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
    hits = input('Enter the number of "Hits" for the player to add: ')
    while not hits.isdigit():
        print('Invalid input. Please enter a valid number for hits.')
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
    print("Edit player stats option, on ui.py")

def move_player():
    print("Move player option, on ui.py")

#load_players()  # delete after testing
#display_lineup()  # delete after testing