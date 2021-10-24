# The aim of this code is to generate the shifts for CucinOne
# © Lorenzo Lagostina
# © Luca Musumeci
# For issues contact musluca.lock@gmail.com
import sys

from users.user_management import obtain_users
from users.user_management import update_users
from users.user_management import write_users
from priority.weight_priority import obtain_extraction_list_threshold
from priority.randomizer import randomize
from slots.shifts_factory import create_shifts_threshold
from common.format_date import date_to_print
from common.shift_utilities import define_heavy_and_light_shifts
from common.shift_utilities import compute_maximum


def calculate_shift():
    # Remove the name of the file, which is always the first arguments
    args = sys.argv[1:]

    # Collect year and month for the shifts
    year = args[0]
    month = args[1]

    # Define the Days and the respective type of shift
    # Example: Mon-2 means that on Monday two person need to do the shift
    # Syntax should be Mon-2;Fri-3 and so on
    shifts_of_week = args[2]

    # Count maximum number of person in a shift this month
    max_num_person = compute_maximum(shifts_of_week)

    num_person_light_shift, num_person_heavy_shift = define_heavy_and_light_shifts(shifts_of_week)

    # Read the users from file csv
    users = obtain_users("./database/users.csv")

    # Obtain the list of users by priority and randomize the order
    extraction_list = obtain_extraction_list_threshold(users, "Low")
    extraction_list = randomize(extraction_list)

    # Create the shifts
    shifts = create_shifts_threshold(year, month, shifts_of_week, extraction_list, users)

    # Update the users and write the CSV
    update_users(users, shifts, num_person_light_shift, num_person_heavy_shift)
    write_users('./database/users.csv', users)

    with open('./database/shifts_' + month + '_' + year + '.txt', mode='w') as latex_table:

        for shift in shifts:
            date = date_to_print(shift[0])
            user_list = []
            empty_cell = ""

            for user in shift[1]:
                user_list.append(user.name)

            if len(user_list) < max_num_person:
                num_empty_cell = max_num_person - len(user_list)

                for _ in range(0, num_empty_cell):
                    empty_cell = empty_cell + "\t&\t"

            latex_table.write(date + '\t&' + '\t&\t'.join(user_list) + empty_cell + '\\\\\\hline\n')


if __name__ == '__main__':
    calculate_shift()
