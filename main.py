# The aim of this code is to generate the shifts for CucinOne
# © Lorenzo Lagostina
# © Luca Musumeci
# © Andrea Torrengo
# For issues contact musluca.lock@gmail.com
from collections import UserList
import sys
from console.console_menu import console_menu_handler
from users.user_management import obtain_users

if __name__ == '__main__':
    # Score of a light, heavy and hood shift
    shift_scores = [2, 3, 6]
    USERS_FILE_PATH = "./database/users.csv"
    # Read the users from file csv
    users = obtain_users(USERS_FILE_PATH)
    if users == None:
        print(" (!) Could not read file \"%s\"" %USERS_FILE_PATH)
    else:
        # Let the user manually enter input values
        console_menu_handler(users, USERS_FILE_PATH, shift_scores)

        # Quick launch, for debug purposes
        # args = sys.argv[1:]
        # calculate_shift(args[0], args[1], args[2], args[3], users)
