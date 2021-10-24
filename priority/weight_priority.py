# There are two different methods to define the weight for every person:

import math


# First way
# The weight is computed with the admonition formula.
# People will be extracted from a shuffled list with all the names
# Someone could be picked up every month if he is unlucky
def define_weight_with_admonition(user):

    admonitions = int(user.admonitions)

    if admonitions == 0 or admonitions == 1:
        return 1
    else:
        # Scale the admonitions to apply the formulas
        punitive = int(user.admonitions) - 2

        multiplier = int(punitive / 3) + 1
        position = punitive % 3 + 1

        # Default value is one because at least one element should be inside the priority queue
        amount_of_shifts = 1

        while multiplier != 0:
            amount_of_shifts = amount_of_shifts + (multiplier * position)
            multiplier -= 1
            position = 3

        amount_of_shifts = amount_of_shifts - int(user.heavy_punitive_shifts) - int(user.light_punitive_shifts)

        return amount_of_shifts if amount_of_shifts != 0 else 1


def obtain_extraction_list_admonitions(users):

    extraction_list = []

    for user in users:
        weight = define_weight_with_admonition(user)

        # Add the user multiple time based on the weights
        for _ in range(int(weight)):
            extraction_list.append(user)

    return extraction_list


# Second way
# A threshold is set up. Person which number of shifts are lesser or higher than threshold will be selected
def obtain_extraction_list_threshold(users, type_of_sample):

    extraction_list = []
    total = 0

    # Obtain the number of person that cleaned in the past for every month
    for user in users:
        total += int(user.light_shifts) + int(user.heavy_shifts)

    threshold = math.ceil(total/len(users))

    for user in users:

        number_of_shifts = int(user.light_shifts) + int(user.heavy_shifts)

        if type_of_sample == "Low":
            if number_of_shifts < threshold:
                extraction_list.append(user)

        else:
            if number_of_shifts >= threshold:
                extraction_list.append(user)

    return extraction_list
