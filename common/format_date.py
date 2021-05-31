# Define the dictionary to convert day_of_week in a number
def convert_day(day_of_week):
    day_map = {
        "Mon": 0,
        "Tue": 1,
        "Wed": 2,
        "Thu": 3,
        "Fri": 4,
        "Sat": 5,
        "Sun": 6
    }
    return day_map[day_of_week]


def convert_num(num):
    day_map = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun"
    }
    return day_map[num]


def date_to_print(date):
    final_date = []

    for element in range(3):
        final_date.append(str(date[element]))

    final_date.reverse()
    final_date = '/'.join(final_date)
    final_date = final_date + ' ' + convert_num(date[3])

    return final_date
