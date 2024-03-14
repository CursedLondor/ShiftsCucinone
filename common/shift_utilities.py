from collections import UserList
from common.format_date import convert_day, date_to_print, monthint_to_string, date_to_print_ita, convert_month_num_ita
from users.user_management import user_find_by_name


# Finds the maximum number of people needed for a shift
def compute_maximum(shifts_of_week):
    # Define max amount of users
    max_amount_users = 0

    # Split the days from the number of users, so it could be process in the code
    shifts_of_week = shifts_of_week.split(';')

    # Loop in the days that have been selected to make the shifts
    for key in shifts_of_week:
        # Extract the day of the shifts
        single_pattern = key.split('-')
        num_users = int(single_pattern[1])
        max_amount_users = max(max_amount_users, num_users)

    return max_amount_users

# Exports shifts into .txt and .latex files
def write_shifts(year, month, max_num_person, shifts):
    latex_start_string = ""
    latex_end_string = ""
    try:
        latex_start_file = open('./common/latex_export/start_string_latex.txt')
        latex_end_file = open('./common/latex_export/end_string_latex.txt')
        latex_start_string = (''.join(latex_start_file.readlines())).strip() + ' '
        latex_end_string = ' ' + (''.join(latex_end_file.readlines())).strip()

        # Add month to title
        substr = "Turni di pulizia"
        index_substring = latex_start_string.find(substr)
        if index_substring != -1:
            index_substring += len(substr)
            latex_start_string = latex_start_string[:index_substring] + " " + convert_month_num_ita(month) + latex_start_string[index_substring:]

        latex_start_file.close()
        latex_end_file.close()
    except:
        print("\n (!) Could not find header and footer for latex file")

    # Write .txt file
    with open('./database/shifts_' + str(year) + '_' + monthint_to_string(month) + '.txt', mode='w', encoding='utf-8') as txt_file:
        # Write Latex file
        with open('./database/shifts_' + str(year) + '_' + monthint_to_string(month) + '_latex.txt', mode='w', encoding='utf-8') as latex_table:
            # Write "header" into latex file
            latex_table.write(latex_start_string)
            for shift in shifts:
                user_list = []
                user_role = []
                empty_cell = ""
                # used in general
                date_eng = date_to_print(shift[0])
                # only used to print on latex file
                date_ita = date_to_print_ita(shift[0])

                for user in shift[1]:
                    user_list.append(user.name)
                
                for role in shift[2]:
                    user_role.append(role)

                if len(user_list) < max_num_person:
                    num_empty_cell = max_num_person - len(user_list)

                    for _ in range(0, num_empty_cell):
                        empty_cell = empty_cell + "\t&\t"

                txt_line = date_eng + ';' + ','.join(user_list) + ';' + ','.join(user_role) + ';' + shift[3] + '\n'
                if shift[3] == 'hood':
                    latex_line = ' \\vspace{4\\baselineskip}\\\\Turno cappa: \\\\\\hline ' + date_ita + '\t&' + '\t&\t'.join(user_list) + empty_cell + '\\\\\\hline\n'
                else:
                    latex_line = date_ita + '\t&' + '\t&\t'.join(user_list) + empty_cell + '\\\\\\hline\n'
                txt_file.write(txt_line)
                latex_table.write(latex_line)
            # Write "footer" into latex file
            latex_table.write(latex_end_string)
            latex_table.close()
        txt_file.close()
    print("\n >> File \"%s\" saved successfully" %('./database/shifts_' + str(year) + '_' + monthint_to_string(month) + '.txt'))


# Returns shifts list and hood shift
# shifts = [[day_tuple][users_list]]
def read_shifts(year, month, users):
    shifts = []
    # Number of people in a light and heavy shifts
    n_people_light = 1000
    n_people_heavy = 0

    try:
        txt_file = open('./database/shifts_' + str(year) + '_' + monthint_to_string(month) + '.txt', mode='r', encoding='utf-8')
    except:
        print(" File \"%s\" does not exists" %('./database/shifts_' + str(year) + '_' + monthint_to_string(month) + '.txt'))
        return shifts, n_people_light, n_people_heavy
    lines = txt_file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
        # if empty line, skip to next line
        if lines[i] != "":
            pattern = lines[i].split(';')
            # date tuple: (yyyy, mm, dd, NumDayOfWeek)
            date_str_array = pattern[0].split(' ')
            date_int_array = [int(key) for key in date_str_array[0].split('/')]
            date_int_array.append(convert_day(date_str_array[1]))

            date_tuple = (date_int_array[2], date_int_array[1], date_int_array[0], date_int_array[3])
            user_names = [usr for usr in pattern[1].split(',')]
            user_roles = [role for role in pattern[2].split(',')]
            shift_type = pattern[3]
            users_list = []
            # Get user data from users object
            for name in user_names:
                usr = user_find_by_name(users, name)
                if usr is None:
                    print(" [Critical Error](!) Couldn't find user \"%s\" inside \"users.csv\"." %name)
                    return None, None, n_people_light, n_people_heavy
                else:
                    users_list.append(usr)
            if len(users_list) > n_people_heavy:
                n_people_heavy = len(users_list)
            if len(users_list) < n_people_light:
                n_people_light = len(users_list)
                
            shifts.append([date_tuple, users_list, user_roles, shift_type])
    txt_file.close()
    
    return shifts, n_people_light, n_people_heavy

# Given a date tuple, return index of the shift list
def shift_get_index_of(shifts, date_tuple):
    hood_date = False
    found = -1
    # Check if date_tuple is a hood_shift
    j = len(shifts) - 1
    if date_tuple[0] == shifts[j][0][0] and date_tuple[1] == shifts[j][0][1] and date_tuple[2] == shifts[j][0][2]:
        hood_date = True

    # Finds the index of the requested shift (light/heavy/hood)
    for i in range(len(shifts) - 1):
        if date_tuple[0] == shifts[i][0][0] and date_tuple[1] == shifts[i][0][1] and date_tuple[2] == shifts[i][0][2]:
            found = i
    
    if hood_date == True and found == -1:
        return j

    if hood_date == True and found != -1:
        choice = -1
        print("\n This date refers to both regular shift and hood shift. Choose what you want to select:")
        print(" [1] Regular shift (light or heavy)")
        print(" [2] Hood shift\n")
        valid = False
        while choice < 1 or choice > 2 or valid == False:
            try:
                choice = int(input(' Choice: '))
                valid = True
            except:
                print(" (!) Please insert a number")
                valid = False
        
        if choice == 2:
            return j
    
    return found

# Return the index of the field of the user to update
def get_users_field_index_to_update(user_role, shift_type):
    start_index = 2
    type_contribute = 0
    role_contribute = 0
    if shift_type == "light":
        type_contribute = 0
    elif shift_type == 'heavy':
        type_contribute = 1
    else:
        type_contribute = 2
    
    if user_role == 'r':
        role_contribute = 0
    else:
        role_contribute = 1
    return start_index + type_contribute + 3 * role_contribute
