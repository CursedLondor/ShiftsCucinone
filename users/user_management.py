import csv
from fileinput import filename
import math
from common.format_date import is_datestring_valid, is_ddmm_valid

from users.user import User


def obtain_users(file_name):
    # Open the file that will contain the users
    try:
        with open(file_name, encoding='utf-8') as csv_file:

            # Initialize the csv reader
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Skip the header
            next(csv_reader)

            users = []

            for row in csv_reader:
                # Add every user in a dictionary to avoid name duplicate
                users.append(
                    User(row[0], row[1], row[2], row[3], row[4],
                        row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

        return users
    except:
        return None


def write_users(file_name, users):
    # Open the file that will contain the users
    with open(file_name, mode='w', newline='', encoding='utf-8') as users_file:

        # Initialize the csv writer
        csv_writer = csv.writer(users_file, delimiter=',')

        # Write the header
        csv_writer.writerow(['Name', 'Charisma', 'Light Shifts', 'Heavy Shifts', 
                    'Hood Shifts', 'Light Punitive Shifts', 'Heavy Punitive Shifts',
                    'Hood Punitive Shifts', 'Admonitions', 'Remaining Admonitions', 'Availability', 'Forbidden Links'])

        
        # Update all the students
        for user in users:
            # Re-Join dates array for each user
            str_array = [str(key) for key in user.availability]
            # Sort string array
            str_array.sort(reverse=False)
            str_availability = ';'.join(str_array)
            csv_writer.writerow([user.name, user.charisma, user.light_shifts, 
                user.heavy_shifts, user.hood_shifts, user.light_punitive_shifts, 
                user.heavy_punitive_shifts, user.hood_punitive_shifts, 
                user.admonitions, user.remaining_admonitions, str_availability, 
                user.forbidden_links])
    
    users_file.close()
    print("\n >> File \"%s\" saved successfully" %(file_name))


def is_a_punitive_shift(encountered_users, user):
    for enc_usr in encountered_users:
        if user.name == enc_usr.name:
            return True
    return False


def increment(user, is_light_shift, is_punitive):
    # Check if this is a punitive shifts
    if is_punitive:
        # Update punitive shifts for that user
        if is_light_shift:
            user.light_punitive_shifts = int(user.light_punitive_shifts) + 1
        else:
            user.heavy_punitive_shifts = int(user.heavy_punitive_shifts) + 1
    else:
        # Update the shifts for that user
        if is_light_shift:
            user.light_shifts = int(user.light_shifts) + 1
        else:
            user.heavy_shifts = int(user.heavy_shifts) + 1


""" def update_users(users, shifts, light, heavy):
    # A list of encountered users during the loop in shifts
    encountered_users = set()

    # Cycle the users for every shift
    for shift in shifts:

        # Verify the type of shift (heavy or light)
        is_light_shift = True
        if len(shift[1]) == heavy:
            is_light_shift = False

        for shift_user in shift[1]:
            # @AT: That's not the optimal way to verify if a shift is punitive:
            # 1) The user may have only one "punitive" turn in the current month, however it would count as "normal turn"
            # 2) Lazzari usually keeps admonished users for cleaning the hood of the kitchen

            # It would be better to provide the possibility to add admonitions directly through the file

            # @LM: In case there is at least one element inside the encountered list
            if encountered_users:
                ###########################################
                #### Edit 28.10.2022 - Andrea Torrengo ####
                ###########################################
                # Code Optimization

                # If true, this is a punitive shift
                ret = is_a_punitive_shift(encountered_users, shift_user)
                for user in users:
                    if user.name == shift_user.name:
                        increment(user, is_light_shift, ret)
                        break

            # In case the list is empty, consider the shift as normal shift
            else:
                for user in users:
                    if user.name == shift_user.name:
                        # Update the shifts for that user
                        if is_light_shift:
                            user.light_shifts = int(user.light_shifts) + 1
                        else:
                            user.heavy_shifts = int(user.heavy_shifts) + 1
                        break

            encountered_users.add(shift_user)
"""

def get_exception_dates_list():
    exception_dates_list = []

    with open("./database/exception_dates_list.txt", "r", encoding='utf-8') as txtFile:
        # Ignore first line
        txtFile.readline()
        content = txtFile.readlines()
        for line in content:
            line = line.replace("\n", "")
            # Check if line is a valid date
            if is_ddmm_valid(line):
                exception_dates_list.append(line)
            else:
                print(" (!) %s is not a valid date" %line)
        txtFile.close()

    return exception_dates_list


# Caution: this function deletes users data inside the .csv file
# Must only be called at the end of the college period (August)
def user_data_delete(users, file_name):
    for user in users:
        user.charisma = 10
        user.light_shifts = 0
        user.heavy_shifts = 0
        user.hood_shifts = 0
        user.light_punitive_shifts = 0
        user.heavy_punitive_shifts = 0
        user.hood_punitive_shifts = 0
        user.admonitions = 0
        user.remaining_admonitions = 0
        user.availability = []
    write_users(file_name, users)

# username must be the exact full name of the user
def user_find_by_name(users, username):
    for user in users:
        if(str(user.name).lower() == str(username).lower()):
            return user
    return None

# Returns a list of users, which full name matches with the user substring
def users_find_by_substring(users, user_substring):
    found_users = []
    for user in users:
        if(user_substring in str(user.name).lower()):
            found_users.append(user)
    return found_users

def user_get_index_of(users, usr):
    i = 0
    for i in range(len(users)):
        if(str(usr.name).lower() == str(users[i].name).lower()):
            return i
    return -1

def user_incr_admonitions(user):
    user.admonitions += 1
    user.remaining_admonitions += 1

def user_decr_admonitions(user):
    if user.remaining_admonitions > 0:
        user.remaining_admonitions -= 1

def user_remove(users, index):
    users.pop(index)

# Add new user, mantaining order by username
def user_add(users, usr):
    # append user
    users.append(usr)
    # insertion sort to the last user
    i = len(users) - 1
    aux = users[i]
    i -= 1
    while i >= 0 and aux.name.lower() < users[i].name.lower():
        users[i + 1] = users[i]
        i -= 1
    users[i + 1] = aux

def user_get_score(user, shift_score):
    return int(user.light_shifts) * shift_score[0] + int(user.heavy_shifts) * shift_score[1] + int(user.hood_shifts) * shift_score[2]

# sorts a user list by lowest scores
def user_sort_list_by_score(users, shift_scores):
    # get and save users scores in a list
    scores = []
    i = 1
    for user in users:
        scores.append(user_get_score(user, shift_scores))
    # sort each user (and corresponding score) by lowest scores
    # insertion sort
    while i < len(users):
        aux_score = scores[i]
        aux_user = users[i]
        j = i - 1
        while j >= 0 and scores[j] > aux_score:
            scores[j + 1] = scores[j]
            users[j + 1] = users[j]
            j -= 1
        scores[j + 1] = aux_score
        users[j + 1] = aux_user
        i += 1
    


def user_get_threshold(users, shift_scores):
    total = 0
    for user in users:
        total += user_get_score(user, shift_scores)
    return math.ceil(total/len(users))

def user_increment_field_value(users_list, index_list, index_field, increment):
    if index_field == 1:
        users_list[index_list].charisma += increment
    elif index_field == 2:
        users_list[index_list].light_shifts += increment
    elif index_field == 3:
        users_list[index_list].heavy_shifts += increment
    elif index_field == 4:
        users_list[index_list].hood_shifts += increment
    elif index_field == 5:
        users_list[index_list].light_punitive_shifts += increment
    elif index_field == 6:
        users_list[index_list].heavy_punitive_shifts += increment
    elif index_field == 7:
        users_list[index_list].hood_punitive_shifts += increment
    elif index_field == 8:
        users_list[index_list].admonitions += increment
    elif index_field == 9:
        users_list[index_list].remaining_admonitions += increment
    else:
        print(" (!) Couldn't increment any field with index %d" %(index_field))