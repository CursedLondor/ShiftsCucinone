# There are two ways to create shifts

import calendar
from common.format_date import convert_day, get_current_date_string, get_week_day
from priority.weight_priority import get_available_people_for_date, split_av_and_na_users, obtain_extraction_list_admonished, obtain_extraction_list_admonitions, obtain_extraction_list_threshold
from users.user_management import user_decr_admonitions, user_get_index_of, user_increment_field_value, user_sort_list_by_score



from jinja2 import Undefined
from sqlalchemy import null

from users.user_management import get_exception_dates_list
from users.user_management import write_users
from priority.randomizer import randomize
from common.format_date import date_to_print
from common.shift_utilities import define_heavy_and_light_shifts, get_users_field_index_to_update, write_shifts
from common.shift_utilities import compute_maximum


def calculate_shift(year, month, shifts_of_week, hood_shift_string, users, USERS_FILE_PATH, shift_scores):
    # Collect year and month for the shifts
    #year = int(year)
    #month = int(month)

    # Shift of Week:
    # Define the Days and the respective type of shift
    # Example: Mon-2 means that on Monday two person need to do the shift
    # Syntax should be Mon-2;Fri-3 and so on

    # (Optional) Hood Shift String (else "")
    # Get the day number for hood cleaning shift (introduced in October 2022)
    # Syntax should be, for example, 12-3
    # which means on date 12/month/year there will be a hood shift made of 3 people

    # Get dates to be avoided for shift generations (ie: Holidays)
    exception_dates_list = get_exception_dates_list()

    # Count maximum number of person in a shift this month
    max_num_person = compute_maximum(shifts_of_week)

    #num_person_light_shift, num_person_heavy_shift = define_heavy_and_light_shifts(shifts_of_week)

    # Create the shifts
    shifts = create_shifts_threshold(year, month, shifts_of_week, users, exception_dates_list, hood_shift_string, shift_scores, max_num_person)

    # Update the users and write the CSV
    # update_users(users, shifts, num_person_light_shift, num_person_heavy_shift)
    write_users(USERS_FILE_PATH, users)

    write_shifts(year, month, max_num_person, shifts)
    


# This function has changed a lot, since the last development
# Note: the purpose of this program is to assign shifts to only available people
# For now, not available people lists are not used
# The extraction algorithm uses a Greedy approach, it only takes optimal local solutions:
# the assign of the shift won't be always optimal, because it does not consider the whole 
# possible choices.
# Example: John is available on 5/12/ and 7/12. Paul is the only one person available on 7/12 (double-shift).
# John is assigned to 5/12
# Paul is assigned to 7/12
# ==> assigments are not optimal, John could have been assigned to 7/12
def create_shifts_threshold(year, month, shifts_of_week, original_users, exception_dates_list, hood_shift_string, shift_scores, max_num_people):
    regular_role = 'r'
    punitive_role = 'p'
    backup_file_path = './database/backup/users_backup_' + str(get_current_date_string()) + '.csv'

    # Most important thing: backup users.csv
    print(" Backing up users...")
    write_users(backup_file_path, original_users)

    # Create the shifts list. A shift contains the day of the shift and people who need to do the shift
    shifts = []
    chosen_users = []
    hood_shift = []

    # Set up integer from string
    year = int(year)
    month = int(month)

    # Split the days from the number of users, so it could be process in the code
    shifts_of_week = shifts_of_week.split(';')

    # Create the calendar starting from Monday (if the current month does not starts with a Monday
    # the calendar will contain days from the previous month. The same if the current month does
    # not end with a Sunday
    cal = calendar.Calendar(firstweekday=0)
    
    # Obtain the list of users who have at least one admonition to discount
    admonished_list = obtain_extraction_list_admonished(original_users)
    randomize(admonished_list)
    # Obtain the list of low-score users (after randomize, sort users by lowest Low scores)
    low_score_list = obtain_extraction_list_threshold(original_users, "Low", shift_scores)
    randomize(low_score_list)
    # Obtain the list of high-score users (after randomize, sort users by lowest High scores)
    high_score_list = obtain_extraction_list_threshold(original_users, "High", shift_scores)
    randomize(high_score_list)

    ######################################################
    # Check if a hood shift is scheduled this month
    # Important note: this shift will be stored at the end of shifts list
    if hood_shift_string != "":
        pattern = hood_shift_string.split("-")
        date_string = str(pattern[0]) + '/' + str(month) + '/' + str(year)
        hood_date_tuple = (year, month, int(pattern[0]), get_week_day(date_string))
        hood_num_people = int(pattern[1])

        # Integer Hood Date
        int_date = year * 10000 + month * 100 + int(pattern[0])
        # Split available users and not available users
        ulist_av_adm, ulist_na_adm = split_av_and_na_users(admonished_list, int_date)
        ulist_av_low, ulist_na_low = split_av_and_na_users(low_score_list, int_date)
        ulist_av_high, ulist_na_high = split_av_and_na_users(high_score_list, int_date)
        # Sort lists by lower scores
        user_sort_list_by_score(ulist_av_adm, shift_scores)
        user_sort_list_by_score(ulist_av_low, shift_scores)
        user_sort_list_by_score(ulist_av_high, shift_scores)

        # Get people available on hood shift day
        i = 0
        chosen_users = []
        user_role = []
        while(i < hood_num_people):
            temp_usr = None
            temp_role = regular_role
            i += 1
            # First pick available admonished people
            if(len(ulist_av_adm) > 0):
                temp_usr = ulist_av_adm.pop(0)
                # also remove the user in admonished_list
                admonished_list.remove(temp_usr)
                # indicates that the user is doing a PUNITIVE shift
                temp_role = punitive_role
                # Decrease number of remaining admonitions
                index = user_get_index_of(original_users, temp_usr)
                user_decr_admonitions(original_users[index])

            # Then pick available low-score-people
            elif(len(ulist_av_low) > 0):
                temp_usr = ulist_av_low.pop(0)
                low_score_list.remove(temp_usr)
                # indicates that the user is doing a REGULAR shift
                temp_role = regular_role
            # Eventually pick available high-score-people
            elif(len(ulist_av_high) > 0):
                temp_usr = ulist_av_high.pop(0)
                high_score_list.remove(temp_usr)
                temp_role = regular_role
            # Worst case scenario: not enough people
            else:
                i = hood_num_people
            
            # If a user has been added, calculate score
            if temp_usr != None:
                chosen_users.append(temp_usr)
                user_role.append(temp_role)
                user_index = user_get_index_of(original_users, temp_usr)
                field_index = get_users_field_index_to_update(temp_role, 'hood')
                user_increment_field_value(original_users, user_index, field_index, 1)

        # date of the shift; user_list; user_role; shift_type (hood/light/heavy)
        hood_shift = [hood_date_tuple, chosen_users, user_role, 'hood']
    ######################################################
    

    for day_tuple in cal.itermonthdays4(int(year), int(month)):
        ddmm = str(day_tuple[2]) + '/' + str(day_tuple[1])
        shift_days_of_week = [
            [convert_day(str(key).split('-')[0]), int(str(key.split('-')[1]))] 
            for key in shifts_of_week]
        
        # @AT: I added a function to:
        # check whether this day is a shift day or not
        index = get_index_shift_of_week(shift_days_of_week, day_tuple[3])

        # Select only the shift days of the current month, except certain dates (ie: Holidays)
        if day_tuple[1] == month and index != -1 and ddmm not in exception_dates_list:
            # Extract the users from the priority list
            num_users = (shift_days_of_week[index])[1]
            chosen_users = []
            user_role = []
            temp_usr = None
            temp_role = regular_role
            i = 0

            shift_type = ""
            if num_users == max_num_people:
                shift_type = 'heavy'
            else:
                shift_type = 'light'

            # For each shift date, split available and not available people
            int_date = year * 10000 + month * 100 + int(day_tuple[2])
            ulist_av_adm, ulist_na_adm = split_av_and_na_users(admonished_list, int_date)
            ulist_av_low, ulist_na_low = split_av_and_na_users(low_score_list, int_date)
            ulist_av_high, ulist_na_high = split_av_and_na_users(high_score_list, int_date)
            # Sort lists by lower scores
            user_sort_list_by_score(ulist_av_adm, shift_scores)
            user_sort_list_by_score(ulist_av_low, shift_scores)
            user_sort_list_by_score(ulist_av_high, shift_scores)

            while i < int(num_users):
                i += 1

                # Considering a shift date:
                # First, assign shifts to available low-score people
                # Then, assign shifts to available admonished people
                # Eventually assign shifts to available high-score people
                # 
                # Then, assign unavailable admonished people
                # Eventually assign unavailable low and high score people
                # 
                # Worst case scenario: not enough people for that shift date


                # First pick available low-score-people
                if(len(ulist_av_low) > 0):
                    temp_usr = ulist_av_low.pop(0)
                    temp_role = regular_role
                    low_score_list.remove(temp_usr)
                # Then pick available admonished people
                elif(len(ulist_av_adm) > 0):
                    temp_usr = ulist_av_adm.pop(0)
                    temp_role = punitive_role
                    index = user_get_index_of(original_users, temp_usr)
                    user_decr_admonitions(original_users[i])
                    admonished_list.remove(temp_usr)
                # Then pick available high-score-people
                elif(len(ulist_av_high) > 0):
                    temp_usr = ulist_av_high.pop(0)
                    temp_role = regular_role
                    high_score_list.remove(temp_usr)
                # Then pick unavailable admonished people (useless)
                #elif(len(ulist_na_adm) > 0):
                #    temp_usr = ulist_na_adm.pop(0)
                #    temp_role = punitive_role
                #    index = user_get_index_of(original_users, temp_usr)
                #    user_decr_admonitions(original_users[i])
                #    admonished_list.remove(temp_usr)
                ## Then pick unavailable low-score people
                #elif(len(ulist_na_low) > 0):
                #    temp_usr = ulist_na_low.pop(0)
                #    temp_role = regular_role
                #    low_score_list.remove(temp_usr)
                ## Then pick unavailable high-score people
                #elif(len(ulist_na_high) > 0):
                #    temp_usr = ulist_na_high.pop(0)
                #    temp_role = regular_role
                #    high_score_list.remove(temp_usr)
                ## Worst case scenario: not enough people
                else:
                    i = max_num_people + 1
                    print("\n (!) Not enough people for shift of %s" %ddmm)
            
            
                if i != max_num_people + 1:
                    chosen_users.append(temp_usr)
                    user_role.append(temp_role)

                    # Update temp_usr score
                    temp_usr_index = user_get_index_of(original_users, temp_usr)
                    field_index = get_users_field_index_to_update(temp_role, shift_type)
                    user_increment_field_value(original_users, temp_usr_index, field_index, 1)

            # Populate the shifts
            shifts.append([day_tuple, chosen_users, user_role, shift_type])

    # Append hood shift at the end of shifts
    if len(hood_shift) > 0:
        shifts.append(hood_shift)
    return shifts

def get_index_shift_of_week(shift_days_of_week, day):
    i = 0
    for i in range(len(shift_days_of_week)):
        if(shift_days_of_week[i][0] == day):
            return i
    return -1