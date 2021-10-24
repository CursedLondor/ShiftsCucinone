def define_heavy_and_light_shifts(pattern):
    # Compute the number of users for light and heavy shift
    persons_in_turn = []

    pattern = [pat.split('-') for pat in pattern.split(';')]
    for element in pattern:
        persons_in_turn.append(int(element[1]))

    return min(persons_in_turn), max(persons_in_turn)


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
