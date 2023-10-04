
# Returns an integer
from ast import While

from common.format_date import (dateint_to_string, datestring_to_int, get_date_list_by_dow,
                                get_date_list_by_range,
                                get_end_of_academic_year, is_datestring_valid,
                                is_day_of_week_string)
from common.shift_utilities import (get_users_field_index_to_update,
                                    read_shifts, shift_get_index_of,
                                    write_shifts)
from priority.weight_priority import obtain_extraction_list_admonished, obtain_extraction_list_threshold
from slots.shifts_factory import calculate_shift
from users.user import User
from users.user_management import (obtain_users, user_add, user_data_delete,
                                   user_find_by_name, user_get_index_of, user_get_score, user_get_threshold,
                                   user_incr_admonitions,
                                   user_increment_field_value, user_remove, user_sort_list_by_score,
                                   users_find_by_substring, write_users)


def console_menu_print():
    choice = -1
    print("")
    print(" " + "-" * 40)
    print(" [1] : Generate shifts")
    print(" [2] : Users management")
    print(" [0] : Quit")
    print(" " + "-" * 40)
    
    while choice < 0 or choice > 2:
        try:
            choice = int(input(" Choice: "))
        except:
            print(" (!) Invalid choice")

    return choice

def user_menu_print():
    choice = -1
    print(" " + "-" * 40)
    print(" [1] : Admonite user")
    print(" [2] : Show user")
    print(" [3] : Show users scores")
    print(" [4] : Edit user availability")
    print(" [5] : Swap users shifts")
    print(" [6] : Add new user")
    print(" [7] : Remove existing user")
    print(" [8] : Delete all users data")
    print(" [9] : Debug only")
    print(" [0] : Back")
    print(" " + "-" * 40)
    
    while choice < 0 or choice > 9:
        try:
            choice = int(input(" Choice: "))
        except:
            print(" (!) Invalid choice")
    return choice

def console_menu_wait():
    input("\n\n Press ENTER key to continue...")


def console_menu_handler(users, USERS_FILE_PATH, shift_scores):
    
    choice_main_menu = 1
    while choice_main_menu > 0 and choice_main_menu <= 2:
        choice_main_menu = console_menu_print()

        if choice_main_menu == 1:
            # Calculate Shifts #
            ####################
            valid = False
            print("")
            print(" -------------------------------------------------------------------------------------")
            print(" | CAUTION: Please read this carefully                                               |")
            print(" -------------------------------------------------------------------------------------")
            print(" | This utility allows you to generate shifts, depending on people availability,     |")
            print(" | scores and admonitions. First of all, \"users.csv\" file is backed up into          |")
            print(" | \"/database/backup/users_backup_yyyy-mm-dd_HH-MM-SS.csv\"                           |")
            print(" | After that, the shifts are generated and the number of shifts of each person      |")
            print(" | will immediately be updated.                                                      |")
            print(" |                                                                                   |")
            print(" | IMPORTANT! IF YOU ARE NOT SATISFIED with the resulting shifts,                    |")
            print(" | and want to RE-GENERATE shifts, you MUST:                                         |")
            print(" | 1) close this program                                                             |")
            print(" | 2) go inside \"/database\" folder and move \"users.csv\" to another location          |")
            print(" | 3) go inside \"/database/backup\" folder                                            |")
            print(" | 4) find the most recent backup file \"users_backup_yyyy-mm-dd_HH-MM-SS.csv\"        |")
            print(" | 5) move it to \"/database\" folder                                                  |")
            print(" | 6) rename it to \"users.csv\"                                                       |")
            print(" | 7) reopen this program and generate shifts again                                  |")
            print(" |                                                                                   |")
            print(" | But...why do I have to do this???                                                 |")
            print(" | For restoring users' data before the \"incorrect\" shifts were generated            |")
            print(" -------------------------------------------------------------------------------------")
            print("")
            year = input(" Insert year: ")
            month = input(" Insert month: ")
            while valid == False:
                shift_of_week = input(" Insert <dayname-Npeople> followed by \";\" (ie: mon-2;wed-2;fri-2;sun-3): ")
                # check if inserted days of week are correct
                days_to_check = shift_of_week.split(";")
                if len(days_to_check) > 0:
                    days_to_check = [day.split("-")[0] for day in days_to_check]
                    i = 0
                    valid = True
                    while i < len(days_to_check) and valid == True:
                        valid = is_day_of_week_string(days_to_check[i])
                        i += 1
                    if valid == False:
                        print("\n (!) \"%s\" is not a valid day name" %days_to_check[i - 1])
                else:
                    print("\n (!) Please, insert at least a day name and number of people")

            hood_shift_string = ""
            print("\n Do you want to add a hood shift in this month?")
            c = input("\n [Y/N]: ")
            if c == 'Y' or c == 'y':
                valid = False
                while valid == False:
                    hood_shift_string = input(" Insert <daynumber-Npeople> (ie: 21-3): ")
                    # check if input is correct
                    try:
                        pattern = []
                        pattern = hood_shift_string.split("-")
                        if len(pattern) == 2:
                            dayNumber = int(pattern[0])
                            numPeople = int(pattern[1])
                            dateint = int(year) * 10000 + int(month) * 100 + dayNumber
                            valid = is_datestring_valid(dateint_to_string(dateint))
                            if valid == False:
                                print("\n (!) Invalid day number")
                        else:
                            print("\n (!) Please provide only the requested data")
                    except:
                        print("\n (!) Invalid format")

            calculate_shift(year, month, shift_of_week, hood_shift_string, users, USERS_FILE_PATH, shift_scores)
            print("\n >> Shift generated in \"./database/shifts_" + month + "_" + year + ".txt\"")
        elif choice_main_menu == 2:
            choice_user_menu = 1
            # Users management #
            ####################
            while choice_user_menu > 0 and choice_user_menu <= 7:
                choice_user_menu = user_menu_print()
                selected_users = []
                approved = False

                if choice_user_menu == 1:
                    # Admonite user
                    selected_users, approved = console_multiple_users_select(users, "admonite")

                    if approved:
                        for user in selected_users:
                            i = user_get_index_of(users, user)
                            user_incr_admonitions(users[i])
                        write_users(USERS_FILE_PATH, users)
                elif choice_user_menu == 2:
                    # Show user
                    console_show_users(users, shift_scores)
                elif choice_user_menu == 3:
                    # Show users scores
                    max_str_length = 20
                    users_copy = users.copy()
                    user_sort_list_by_score(users_copy, shift_scores)
                    print("\n Users ordered by current scores:")
                    print(" --------------------------------")
                    for u in users_copy:
                        u_print = u.name
                        if len(u_print) > max_str_length:
                            u_print = u_print[:max_str_length - 3]
                            u_print = str(u_print) + "..."
                        else:
                            u_print = u_print.ljust(max_str_length, ' ')
                        print(" | %s | %d" %(u_print, user_get_score(u, shift_scores)))
                    print("\n Current threshold score: %d" %user_get_threshold(users, shift_scores))
                elif choice_user_menu == 4:
                    # Edit user availability
                    console_edit_user_availability(users, USERS_FILE_PATH)
                elif choice_user_menu == 5:
                    # Swap users shifts
                    shifts = []
                    # Specify the shifts to be modified
                    print(" | Specify the shift file to edit |")
                    valid = False
                    while valid == False:
                        try:
                            year = int(input(" Insert year: "))
                            month = int(input(" Insert month: "))
                            valid = True
                        except:
                            print(" (!) Please, insert a numeric value")
                            valid = False
                    shifts, num_people_light_shift, num_people_heavy_shift = read_shifts(year, month, users)
                    
                    if shifts is None:
                        print("\n (!) You were probably trying to edit an old shift file. That is not possible if you do not have every user registered in \"users.csv\" file")
                    elif len(shifts) == 0:
                        print(" File not Found: Operation aborted")
                    else:
                        console_swap_users(users, shifts, month, year, num_people_light_shift, num_people_heavy_shift, USERS_FILE_PATH)
                elif choice_user_menu == 6:
                    # Add new user
                    console_input_user(users, USERS_FILE_PATH)
                elif choice_user_menu == 7:
                    # Remove existing user
                    selected_users, approved = console_multiple_users_select(users, "permanently remove")

                    if approved is True:
                        for user in selected_users:
                            i = user_get_index_of(users, user)
                            if i != -1:
                                user_remove(users, i)
                                print(" >> User \"%s\" removed successfully" %(user.name))
                            else:
                                print(" (i) User \"%s\" has already been removed (operation skipped)" %(user.name))
                        write_users(USERS_FILE_PATH, users)

                elif choice_user_menu == 8:
                    # Delete users' data
                    print("\n")
                    print(" ###################################################################################")
                    print(" ## (!) Warning: ALL USER DATA WILL BE PERMANENTLY DELETED                        ##")
                    print(" ## This is a one-time confirmation prompt                                        ##")
                    print(" ## Do you really want to reset all users' scores, admonitions and availability?  ##")
                    print(" ###################################################################################")
                    confirm = input(" [Y/N]: ")
                    if confirm == 'y' or confirm == 'Y':
                        print("\n >> Users' data erased")
                        # Write file
                        user_data_delete(users, USERS_FILE_PATH)
                    else:
                        print("\n (operation aborted)")
                elif choice_user_menu == 9:
                    print("\n\n Debug Only -- Admonished people score list")
                    #tmp_user_list = obtain_extraction_list_threshold(users, "Low", shift_scores)
                    tmp_user_list = obtain_extraction_list_admonished(users)
                    for user in tmp_user_list:
                        print(user.name, user_get_score(user, shift_scores))
                    
                    # for u in users:
                    #     print(u.name)
                    # print("-- sorted --")
                    # user_sort_list_by_score(users, shift_scores)
                    # for u in users:
                    #     print(u.name)

                if choice_user_menu != 0 and choice_user_menu != 2:
                    console_menu_wait()
        if choice_main_menu != 0 and choice_main_menu != 2:
            console_menu_wait()


# Returns a list of selected users and a boolean flag to approve/cancel the next operation
# Output_string is just a string that will be shown inside the console confirmation dialog
def console_multiple_users_select(users, output_string):
    selected_users = []
    full_name = "temp"
    approved = False

    print("")
    print(" ----| Multi select mode | -----------------------------------------------")
    print(" | Insert a full name (or a substring) of a person and press ENTER key.   |")
    print(" | Repeat for every person you want to select.                            |")
    print(" | When you are done: press ENTER key again to end selection.             |")
    print(" | Note #1: you can DEselect/REselect a person writing its name again.    |")
    print(" | Note #2: you can type down a partial name (such as \"vanni\" instead     |")
    print(" | of \"Giovanni\", and so on...). If the inserted text matches multiple    |")
    print(" | users, it will be asked which user to select.                          |")
    print(" -------------------------------------------------------------------------\n")

    while full_name != "":
        full_name = input(" (%d selected) Enter a user's full name or substring: " %(len(selected_users)))

        if full_name != "":
            # Try to search for "full_name" in users list
            ret = user_find_by_name(users, full_name)
            if ret is not None:
                if ret not in selected_users:
                    selected_users.append(ret)
                else:
                    selected_users.remove(ret)
            else:
                # Try to search for a substring matching "full_name"
                users_list = users_find_by_substring(users, full_name)
                if len(users_list) == 0:
                    print("\n (!) User \"%s\" does not exists" %(full_name))
                elif len(users_list) == 1:
                    if users_list[0] not in selected_users:
                        selected_users.append(users_list[0])
                    else:
                        selected_users.remove(users_list[0])
                else:
                    print("\n Did you mean ONE of the following users?")
                    for i in range(len(users_list)):
                        print(" [%d]: %s" %(i + 1, users_list[i].name))
                    print(" [0]: None of these. Go gack")
                    valid = False
                    choice = -1
                    while valid == False or choice < 0 or choice > len(users_list) + 1:
                        try:
                            choice = int(input(" Choice: "))
                            valid = True
                        except:
                            valid = False
                            print(" Please, insert an integer")
                    choice -= 1
                    if choice > -1:
                        if users_list[choice] not in selected_users:
                            selected_users.append(users_list[choice])
                        else:
                            selected_users.remove(users_list[choice])

    if len(selected_users) == 1:
        confirm = input("\n Do you want to %s this %d person? [Y/N]: " %(output_string, len(selected_users)))
    elif len(selected_users) > 1:
        confirm = input("\n Do you want to %s these %d people? [Y/N]: " %(output_string, len(selected_users)))
    else:
        confirm = 'N'
    if confirm == 'y' or confirm == 'Y':
        approved = True
    else:
        print("\n (operation aborted)")
    return selected_users, approved

# Returns a single user object
def console_single_user_select(users, full_name):
    # check if the inserted string matches a part of someone's username
    users_list = users_find_by_substring(users, full_name)
    if len(users_list) == 0:
        print("\n (!) User \"%s\" does not exists" %(full_name))
    else:
        if len(users_list) == 1:
            choice = 0
        else:
            print("\n Did you mean ONE of the following users?")
            for i in range(len(users_list)):
                print(" [%d]: %s" %(i + 1, users_list[i].name))
            print(" [0]: None of these. Go gack")
            valid = False
            choice = -1
            while valid == False or choice < 0 or choice > len(users_list) + 1:
                try:
                    choice = int(input(" Choice: "))
                    valid = True
                except:
                    valid = False
                    print(" Please, insert an integer")
            choice -= 1
        if choice > -1:
            return users_list[choice]
    return None

# Add new user to both <users> and .csv file
def console_input_user(users, USERS_FILE_PATH):
    charisma = 10
    num_ls = num_hs = num_hds = num_lps = num_hps = num_hdps = num_adm = num_radm = 0
    name = ""
    print("")
    while name == "":
        name = input(" Insert the user's full name (Surname Firstname): ")
        if user_find_by_name(users, name) is not None:
            print(" (!) User \"%s\" already exists. User names have to be unique." %(name))
            name = ""
    confirm = input(" Do you want to insert existing data (ie: light, heavy shifts, etc...) to \"%s\"?\n [Y/N]: " %(name))
    if confirm == 'y' or confirm == 'Y':
        # Temporary change num_ls type, to do at least one iteration
        num_ls = 0.1
        charisma = 0
        valid = False
        while valid == False:
            try:
                while charisma < 1 or charisma > 10:
                    charisma = int(input(" Insert user's charisma (1 - 10): "))
                num_ls =   int(input(" Insert the number of light shifts: "))
                num_hs =   int(input(" Insert the number of heavy shifts: "))
                num_hds =  int(input(" Insert the number of hood shifts: "))
                num_lps =  int(input(" Insert the number of light punitive shifts: "))
                num_hps =  int(input(" Insert the number of heavy punitive shifts: "))
                num_hdps = int(input(" Insert the number of hood punitive shifts: "))
                num_adm =  int(input(" Insert the total number of admonitions (discounted + not discounted yet): "))
                num_radm = int(input(" Insert the number of admonitions that the user hasn't discounted yet: "))
                valid = True
            except:
                print(" (!) Please, insert numeric values")
                valid = False

    new_user = User(name, charisma, num_ls, num_hs, num_hds, num_lps, num_hps, num_hdps, num_adm, num_radm, "", "")
    user_add(users, new_user)
    print("\n >> User \"%s\" added successfully" %(new_user.name))
    write_users(USERS_FILE_PATH, users)

# Show users utility
def console_show_users(users, shift_scores):
    full_name = "temp"
    string_array = []
    print("")
    print(" ----| Show user | -------------------------------------------")
    print(" | Insert a full name of a person and press ENTER key        |")
    print(" | Repeat for every person you want to inspect               |")
    print(" | When you are done: press ENTER key again to end selection |")
    print(" -------------------------------------------------------------\n")

    while full_name != "":
        full_name = input(" Enter a user's full name (or substring): ")
        if(full_name != ""):
            ret = console_single_user_select(users, full_name)
            if ret != None:
                print(" -" * 40)
                print(" | Name: %s" %(ret.name))
                print(" | Charisma: %s" %(ret.charisma))
                print(" | Number of light shifts:          %s" %(ret.light_shifts))
                print(" | Number of heavy shifts:          %s" %(ret.heavy_shifts))
                print(" | Number of hood shifts:           %s" %(ret.hood_shifts))
                print(" | Number of light punitive shifts: %s" %(ret.light_punitive_shifts))
                print(" | Number of heavy punitive shifts: %s" %(ret.heavy_punitive_shifts))
                print(" | Number of hood punitive shifts:  %s" %(ret.hood_punitive_shifts))
                print(" | Number of admonitions:           %s" %(ret.admonitions))
                print(" | Number of remaining admonitions: %s" %(ret.remaining_admonitions))
                string_array = [str(key % 100) + "/" + str(int((key % 10000)/100)) + "/" + str(int(key/10000)) for key in ret.availability]
                print(" | Not availability dates: %s" %(string_array))
                print(" | Forbidden links: %s" %(ret.forbidden_links))
                print(" | User's score: %d" %(user_get_score(ret, shift_scores)))
                print(" | Threshold (same for every user): %d" %(user_get_threshold(users, shift_scores)))

# Swap users' shifts
def console_swap_users(users, shifts, month, year, num_people_light, num_people_heavy, USERS_FILE_PATH):
    punitive = 'p'
    regular = 'r'
    choice = -1
    shift1_index = user1_index = shift2_index = user2_index = -1

    if shifts[len(shifts) - 1][3] == 'hood':
        num_people_hood = len(shifts[len(shifts) - 1][1])
    else:
        num_people_hood = 0
    
    # First choose the user to swap
    while shift1_index == -1 or user1_index == -1:
        shift1_index, user1_index = select_shift_and_user(shifts, month, year)

    print("\n Choose one of the following options:")
    print(" [1]: Select a replacement user from the shifts of the current month")
    print(" [2]: Select a replacement user from users list")
    print(" [0]: Cancel")
    valid = False
    while valid == False:
        while choice < 0 or choice > 2:
            try:
                choice = int(input("\n Choice: "))
                valid = True
            except:
                valid = False
    
    # Update user's number of shifts
    # Get the index of both users in users list
    user1_list_index = user_get_index_of(users, shifts[shift1_index][1][user1_index])
    user1_field_index = get_users_field_index_to_update(shifts[shift1_index][2][user1_index], shifts[shift1_index][3])

    if choice == 1:
        while shift2_index == -1 or user2_index == -1:
            shift2_index, user2_index = select_shift_and_user(shifts, month, year)

        
        # Decrease u1 and u2 old positions
        user2_list_index = user_get_index_of(users, shifts[shift2_index][1][user2_index])
        user2_field_index = get_users_field_index_to_update(shifts[shift2_index][2][user2_index], shifts[shift2_index][3])
        user_increment_field_value(users, user1_list_index, user1_field_index, -1)
        user_increment_field_value(users, user2_list_index, user2_field_index, -1)
        
        # Increase u1 and u2 new positions (paying attention to the role of the users)
        user1_field_index = get_users_field_index_to_update(shifts[shift1_index][2][user1_index], shifts[shift2_index][3])
        user2_field_index = get_users_field_index_to_update(shifts[shift2_index][2][user2_index], shifts[shift1_index][3])
        user_increment_field_value(users, user1_list_index, user1_field_index, +1)
        user_increment_field_value(users, user2_list_index, user2_field_index, +1)

        # Update shifts
        # Swap users
        user_aux = shifts[shift1_index][1][user1_index]
        shifts[shift1_index][1][user1_index] = shifts[shift2_index][1][user2_index]
        shifts[shift2_index][1][user2_index] = user_aux
        # Swap users' roles
        role_aux = shifts[shift1_index][2][user1_index]
        shifts[shift1_index][2][user1_index] = shifts[shift2_index][2][user2_index]
        shifts[shift2_index][2][user2_index] = role_aux

        # Save users file
        write_users(USERS_FILE_PATH, users)
        # Save shifts file
        write_shifts(year, month, max(num_people_light, num_people_heavy, num_people_hood), shifts)
    elif choice == 2:
        user2_list_index = -1
        while user2_list_index == -1:
            username = input(" Insert the name (or substring) of the replacement user: ")
            temp_user = console_single_user_select(users, username)
            if temp_user != None:
                user2_list_index = user_get_index_of(users, temp_user)
        # Decrement user1 field value (regular or punitive)
        user_increment_field_value(users, user1_list_index, user1_field_index, -1)
        
        # If user1 was doing a punitive shift, increase user1 <remaining_admonitions> field
        if shifts[shift1_index][2][user1_index] == punitive:
            users[user1_list_index].remaining_admonitions += 1

        # If user2 has at least one admonition to discount, mark role as "punitive" and decrease user2 admonitions
        # Otherwise, mark role as "regular"
        if users[user2_list_index].remaining_admonitions > 0:
            shifts[shift1_index][2][user1_index] = punitive
            users[user2_list_index].remaining_admonitions -= 1
            user2_field_index = get_users_field_index_to_update(punitive, shifts[shift1_index][3])
        else:
            shifts[shift1_index][2][user1_index] = regular
            user2_field_index = get_users_field_index_to_update(regular, shifts[shift1_index][3])
        # Increment user2 field value (depending of user2 has admonition to discount, the field will be regular or punitive)
        user_increment_field_value(users, user2_list_index, user2_field_index, +1)

        # Replace user1 to user2
        shifts[shift1_index][1][user1_index] = users[user2_list_index]

        # Save users file
        write_users(USERS_FILE_PATH, users)
        # Save shifts file
        write_shifts(year, month, max(num_people_light, num_people_heavy, num_people_hood), shifts)
    else:
        print("\n Operation aborted")

# Returns the shift index and user index to be swapped
def select_shift_and_user(shifts, month, year):
    valid = False
    while valid == False:
        try:
            day = int(input("\n Insert the day number of the shift: "))
            valid = True
        except:
            valid = False

    date_tuple = (year, month, day)
    i_to_swap = 0

    shift_index = shift_get_index_of(shifts, date_tuple)

    if shift_index != -1:
        print("\n ----| People on %s shift %d/%d/%d |------------" %(shifts[shift_index][3], day, month, year))
        for i in range(len(shifts[shift_index][1])):
            print(" [%d] %s" %(i + 1, (shifts[shift_index][1])[i].name))
        
        print("\n Enter the choice number to select the user to be swapped")
        valid = False
        while valid == False:
            try:
                while i_to_swap < 1 or i_to_swap > len(shifts[shift_index][1]):
                    i_to_swap = int(input(" Choice: "))
                i_to_swap -= 1
                valid = True
            except:
                valid = False
        return shift_index, i_to_swap

    else:
        print(" (!) This is not a shift date")
        return -1, -1

# Add/remove dates in which the user is NOT available
def console_edit_user_availability(users, USERS_FILE_PATH):
    approved = True
    availability_array = []

    while approved == True:
        # select a user (or users)
        selected_users, approved = console_multiple_users_select(users, "select")
        if approved:
            print("")
            print(" Choose one of the following operations:")
            print(" [1]    ADD dates in which the user is NOT available")
            print(" [2] REMOVE dates in which the user is NOT available")
            print(" [0] Back\n")
            valid = False
            while valid == False:
                try:
                    choice = int(input(" Choice: "))
                    valid = True
                except:
                    print(" (!) Invalid choice")
                    valid = False

            if choice == 0:
                approved = False
            else:
                if choice == 1:
                    availability_array = console_select_dates("ADD---")
                    # Update selected users availability (ADD)
                    for user in selected_users:
                        index = user_get_index_of(users, user)
                        for key in availability_array:
                            if key not in users[index].availability:
                                users[index].availability.append(key)

                elif choice == 2:
                    availability_array = console_select_dates("REMOVE")
                    # Update selected users availability (REMOVE)
                    for user in selected_users:
                        index = user_get_index_of(users, user)
                        for key in availability_array:
                            if key in users[index].availability:
                                users[index].availability.remove(key)
                else:
                    print("\n (!) Invalid choice")
    
                # If anything is changed, update users file
                if len(availability_array) > 0:
                    write_users(USERS_FILE_PATH, users)


def console_select_dates(output_string):
    print("\n")
    print(" ----| Select date mode (%s) |-----------------------------------" %output_string)
    print(" | Select the dates in which the selected users are NOT available     |")
    print(" | When you are done: press ENTER key again to go back to select mode |")
    print(" | Accepted input formats:                                            |")
    print(" | (1) single date:   dd/mm/yyyy                                      |")
    print(" | (2) date interval: dd/mm/yyyy dd/mm/yyyy                           |")
    print(" | (3) days of week:  mon tue wed ...                                 |")
    print(" |                                                                    |")
    print(" | Note: days of week option remains active until the end of the      |")
    print(" | academic year (31 August), unless a REMOVE is called for the same  |")
    print(" | days of week.                                                      |")
    print(" ----------------------------------------------------------------------")

    pattern = [""]
    # list of integer dates array
    availability_array = []
    while len(pattern) > 0:
        # user input command
        pattern = input(" (%d days selected) Insert a valid date format: " %len(availability_array))
        # split arguments by spaces
        args = pattern.split(" ")

        if pattern != "":
            # Try to convert first argument as a date
            if is_datestring_valid(args[0]):
                if len(args) > 1:
                    # date interval (Without duplicates)
                    if is_datestring_valid(args[1]):
                        date_string_list = get_date_list_by_range(args[0], args[1])
                        for key in date_string_list:
                            date_int = datestring_to_int(key)
                            if date_int not in availability_array:
                                availability_array.append(date_int)
                    else:
                        print(" (!) Invalid date")
                else:
                    date_int = datestring_to_int(args[0])
                    if date_int not in availability_array:
                        availability_array.append(date_int)
            else:
                # Check if args are days of week
                i = 0
                ok = True
                while i < len(args) and ok:
                    ok = is_day_of_week_string(args[i])
                    i += 1
                if ok:
                    date_string_list = get_date_list_by_dow(args, get_end_of_academic_year())
                    for key in date_string_list:
                        date_int = datestring_to_int(key)
                        if date_int not in availability_array:
                            availability_array.append(date_int)
                else:
                    print(" (!) Invalid format")
    
    return availability_array