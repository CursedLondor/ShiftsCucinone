# There are two different methods to define the weight for every person:

from users.user_management import user_get_score, user_get_threshold

# Second way
# A threshold is set up. Person which number of shifts are lesser or higher than threshold will be selected
# shift_score[0] = light_shift_score (2)
# shift_score[1] = heavy_shift_score (3)
# shift_score[2] = hood_shift_score (6)  # Introduced by the Cucinone meeting in October 2022
def obtain_extraction_list_threshold(users, type_of_sample, shift_score):
    extraction_list = []
    ###########################################
    #### Edit 28.10.2022 - Andrea Torrengo ####
    ###########################################
    # Instead of using the number of shifts, I'm now using a threshold based on
    # assigning a weight for light (=2) and heavy (=3) shifts

    # Obtain the AVERAGE SCORE of people who cleaned in the past months
    threshold = user_get_threshold(users, shift_score)

    for user in users:
        # Computes user's current score
        user_score = user_get_score(user, shift_score)

        if type_of_sample == "Low":
            if user_score < threshold:
                extraction_list.append(user)

        else:
            if user_score >= threshold:
                extraction_list.append(user)

    return extraction_list

# Returns a new list of admonished users
def obtain_extraction_list_admonished(users):
    extraction_list = []
    for user in users:
        if user.remaining_admonitions > 0:
            extraction_list.append(user)
    return extraction_list

# Returns a new list of available users, which are removed from the original list
def get_available_people_for_date(users, integerdate):
    i = 0
    user_list = []
    while i < len(users):
        if integerdate not in users[i].availability:
            user_list.append(users.pop(i))
    return user_list

# Puts available users inside a_list and not available users in na_list
def get_available_users(users, integerdate):
    a_list = []
    #na_list = []
    i = 0
    bottom = len(users) - 1
    while i < len(users) and i <= bottom:
        # If user i is not available on <integerdate>
        if integerdate not in users[i].availability:
            a_list.append(users[i])
        #else:
            # Puts him at the bottom of the list
            #aux = users[i]
            #users[i] = users[bottom]
            #users[bottom] = aux
            ## Must analyse what was in position <bottom>
            #i -= 1
            ## For sure, user at position <bottom> must not be analysed anymore
            #bottom -= 1
            #na_list.append(users[i])
            
        i += 1
    return a_list #, na_list