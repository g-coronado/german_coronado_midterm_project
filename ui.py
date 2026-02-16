from db import list_of_players, VALID_POSITIONS, load_players

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
            print(f'{player_info[0]:<7} {player_info[1]:<21} {player_info[2]:<7} {player_info[3]:<8} {player_info[4]:<6} {player_info[5]}')
               

    except:
        print("Error loading player data from file. Please check the file locationa and structure and try again.")



# Function to display the exit message      
def exit_program():
    print('Goodbye!')



#load_players()  # delete after testing
#display_lineup()  # delete after testing