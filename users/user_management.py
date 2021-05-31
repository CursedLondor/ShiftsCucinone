import csv

from users.user import User


def obtain_users(file_name):
    # Open the file that will contain the users
    with open(file_name) as csv_file:

        # Initialize the csv reader
        csv_reader = csv.reader(csv_file, delimiter=',')
        # Skip the header
        next(csv_reader)

        users = []

        for row in csv_reader:
            # Add every user in a dictionary to avoid name duplicate
            users.append(
                User(row[0], row[1], row[2], row[3], row[4],
                     row[5], row[6], row[7], row[8]))

    return users


def write_users(file_name, users):
    # Open the file that will contain the users
    with open(file_name, mode='w', newline='') as users_file:

        # Initialize the csv writer
        csv_writer = csv.writer(users_file, delimiter=',')

        # Write the header
        csv_writer.writerow(['Name', 'Charisma', 'Light Shift',
                             'Heavy Shift', 'Light Punitive Shifts', 'Heavy Punitive Shifts',
                             'Admonitions', 'Availability', 'Forbidden Links'])

        # Update all the students
        for user in users:
            csv_writer.writerow([user.name, user.charisma, user.light_shifts, user.heavy_shifts,
                                 user.light_punitive_shifts, user.heavy_punitive_shifts, user.admonitions,
                                 user.availability, user.forbidden_links])


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


def update_users(users, shifts, light, heavy):
    # A list of encountered users during the loop in shifts
    encountered_users = set()

    # Cycle the users for every shift
    for shift in shifts:

        # Verify the type of shift (heavy or light)
        is_light_shift = True
        if len(shift[1]) == heavy:
            is_light_shift = False

        for shift_user in shift[1]:

            # In case there is at least one element inside the encountered list
            if encountered_users:
                # If true, this is a punitive shift
                if is_a_punitive_shift(encountered_users, shift_user):
                    for user in users:
                        if user.name == shift_user.name:
                            increment(user, is_light_shift, True)
                            break
                else:
                    for user in users:
                        if user.name == shift_user.name:
                            increment(user, is_light_shift, False)
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
