def define_weight(user):

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


def obtain_extraction_list(users):

    extraction_list = []

    for user in users:
        weight = define_weight(user)

        # Add the user multiple time based on the weights
        for _ in range(int(weight)):
            extraction_list.append(user)

    return extraction_list
