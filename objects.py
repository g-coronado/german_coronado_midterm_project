from baseball_team_manager_viewer import *
from db import *

menu_options = {
        '1': display_lineup,
        '2': add_player,
        '3': remove_player,
        '4': move_player,
        '5': edit_player_position,
        '6': edit_player_status,
        '7': exit_program
    }

while True:
    user_choice = main_menu()
    match user_choice:
        case '1':
            display_lineup()
        case '2':
            add_player()
        case '3':
            remove_player()
        case '4':
            move_player()
        case '5':
            edit_player_position()
        case '6':
            edit_player_status()
        case '7':
            exit_program()
            break
        case _:
            print("That is an invalid option. Please try again and select a valid option from the menu.")

