def define_heavy_and_light_shifts(pattern):
    # Compute the number of users for light and heavy shift
    persons_in_turn = []

    pattern = [pat.split('-') for pat in pattern.split(';')]
    for element in pattern:
        persons_in_turn.append(int(element[1]))

    return min(persons_in_turn), max(persons_in_turn)
