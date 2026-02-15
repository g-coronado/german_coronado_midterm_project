from db import load_players

def display_lineup():
    try:
        print(load_players())
    except:
        print("Error loading player data. Please check the file and try again.")




def main_menu():

        print('===============================================================')
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
        print('C, 1B, 2B, 3B, SS, LF, CF, RF, P')
        print('===============================================================')
        user_choice = input('Please select an option: ')
        return user_choice
      
def exit_program():
    print('Goodbye!')


