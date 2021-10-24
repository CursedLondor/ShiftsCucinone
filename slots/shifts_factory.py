# There are two ways to create shifts

import calendar
from common.format_date import convert_day
from priority.weight_priority import obtain_extraction_list_threshold
from priority.randomizer import randomize


# First Way
# Create shifts based on admonitions
def create_shifts_admonitions(year, month, shifts_of_week, users):
    # Set up integer from string
    year = int(year)
    month = int(month)

    # Create the shifts list. A shift contains the day of the shift and people who need to do the shift
    shifts = []

    # Split the days from the number of users, so it could be process in the code
    shifts_of_week = shifts_of_week.split(';')

    # Create the calendar starting from Monday (if the current month does not starts with a Monday
    # the calendar will contain days from the previous month. The same if the current month does
    # not end with a Sunday
    cal = calendar.Calendar(firstweekday=0)

    for day_tuple in cal.itermonthdays4(int(year), int(month)):

        # Select only the days of the current month
        if day_tuple[1] == month:

            # Loop in the days that have been selected to make the shifts
            for key in shifts_of_week:

                # Extract the day of the shifts
                single_pattern = key.split('-')
                day_of_week = convert_day(single_pattern[0])
                num_users = single_pattern[1]

                # Check if there is a match between the number of the week day and the chosen pattern
                if day_tuple[3] == day_of_week:

                    # Extract the users from the priority list
                    chosen_users = []
                    for _ in range(int(num_users)):
                        # The index that have to be picked up in the users list
                        index = 0

                        # Check if the chosen users is empty
                        if chosen_users:
                            users_without_chosen = list(users)
                            # We need to check if the same user is in the same shift
                            for chosen_user in chosen_users:
                                users_without_chosen = [el for el in users_without_chosen if el != chosen_user]

                            # Find the user in the users list that should be extracted
                            index = users.index(users_without_chosen[0])

                        # Extract the user in position index
                        chosen_users.append(users.pop(index))

                    # Populate the shifts
                    shifts.append([day_tuple, chosen_users])

    return shifts


# Second Way
# Create shifts based on threshold
def create_shifts_threshold(year, month, shifts_of_week, users, original_users):
    # Set up integer from string
    year = int(year)
    month = int(month)

    # Create the shifts list. A shift contains the day of the shift and people who need to do the shift
    shifts = []

    # Split the days from the number of users, so it could be process in the code
    shifts_of_week = shifts_of_week.split(';')

    # Create the calendar starting from Monday (if the current month does not starts with a Monday
    # the calendar will contain days from the previous month. The same if the current month does
    # not end with a Sunday
    cal = calendar.Calendar(firstweekday=0)

    for day_tuple in cal.itermonthdays4(int(year), int(month)):

        # Select only the days of the current month
        if day_tuple[1] == month:

            # Loop in the days that have been selected to make the shifts
            for key in shifts_of_week:

                # Extract the day of the shifts
                single_pattern = key.split('-')
                day_of_week = convert_day(single_pattern[0])
                num_users = single_pattern[1]

                # Check if there is a match between the number of the week day and the chosen pattern
                if day_tuple[3] == day_of_week:

                    # Extract the users from the priority list
                    chosen_users = []
                    for i in range(int(num_users)):
                        try:
                            chosen_users.append(users.pop())
                        except IndexError:
                            i -= 1
                            users = obtain_extraction_list_threshold(original_users, "High")
                            users = randomize(users)

                    # Populate the shifts
                    shifts.append([day_tuple, chosen_users])

    return shifts
