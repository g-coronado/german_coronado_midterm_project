from ui import *
from db import *

db_load_players()
user_choice = display_main_menu()
while True:
    match user_choice:
        case '1':
            display_lineup()
            user_choice = select_option()
        case '2':
            add_player()
            user_choice = select_option()
        case '3':
            remove_player()
            user_choice = select_option()
        case '4':
            move_player()
            user_choice = select_option()
        case '5':
            edit_player_position()
            user_choice = select_option()
        case '6':
            edit_player_stats()
            user_choice = select_option()
        case '7':
            exit_program()
            break
        case _:
            print("That is an invalid option. Please try again and select a valid option from the menu.")
            user_choice = display_main_menu()

