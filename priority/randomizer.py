# This script is used to randomize the list. You cna add a randomizer if you want and call it in the main
import random


def randomize(users):

    for _ in range(random.randint(1, 12)):
        random.shuffle(users)

    return users
