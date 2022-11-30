import datetime

# Define the dictionary to convert day_of_week in a number
def convert_day(day_of_week):
    day_of_week = day_of_week.lower()
    day_map = {
        "mon": 0,
        "tue": 1,
        "wed": 2,
        "thu": 3,
        "fri": 4,
        "sat": 5,
        "sun": 6
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

# Only called for print on latex file
def convert_num_ita(num):
    day_map = {
        0: "Lunedì",
        1: "Martedì",
        2: "Mercoledì",
        3: "Giovedì",
        4: "Venerdì",
        5: "Sabato",
        6: "Domenica"
    }
    return day_map[num]
# Only called for print on latex file
def convert_month_num_ita(num):
    day_map = {
        0: "???",
        1: "Gennaio",
        2: "Febbraio",
        3: "Marzo",
        4: "Aprile",
        5: "Maggio",
        6: "Giugno",
        7: "Luglio",
        8: "Agosto",
        9: "Settembre",
        10: "Ottobre",
        11: "Novembre",
        12: "Dicembre",
    }
    return day_map[num]

# accepts a dd/mm/yyyy date string
def convert_date_string_to_int_array(date_string):
    str_array = date_string.split("/")
    if len(date_string) == 3:
        # Try to convert string elements to int elements
        try:
            day = int(str_array[0])
            month = int(str_array[1])
            year = int(str_array[2])
            return [day, month, year]
        except:
            return None
    else:
        return None

# Check if a string is a day of week
def is_day_of_week_string(str_dow):
    str_dow = str_dow.lower()
    dow_array = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    return str_dow in dow_array

# accepts a dd/mm/yyyy date string
def get_week_day(date_string):
    str_array = date_string.split('/')
    day = int(str_array[0])
    month = int(str_array[1])
    year = int(str_array[2])
    return datetime.date(year, month, day).weekday()
    

def date_to_print(date):
    final_date = []

    for element in range(3):
        final_date.append(str(date[element]))

    final_date.reverse()
    final_date = '/'.join(final_date)
    final_date = final_date + ' ' + convert_num(date[3])

    return final_date

# Accepts a yyyy/mm/dd Dayname string
def date_to_print_ita(date):
    final_date = []
    final_date.append(str(date[2]))
    final_date.append(str(date[1]))

    final_date = '/'.join(final_date)
    final_date = convert_num_ita(date[3]) + ' ' + final_date
    return final_date

def is_datestring_valid(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y')
        return True
    except:
        return False

def is_ddmm_valid(ddmm_date_string):
    end_ay_datestring = get_end_of_academic_year()
    month_input = ddmm_date_string.split('/')[1]
    month_end_ay = end_ay_datestring.split('/')[1]
    try:
        # get current year
        year = int(datetime.date.today().strftime("%Y"))
    except:
        return False
    # if the month is less than end of a.y month (August)
    if month_input < month_end_ay:
        year += 1
    return is_datestring_valid(ddmm_date_string + "/" + str(year))

# accepts a dd/mm/yyyy date string, returns a date-string list
def get_date_list_by_range(start_date, end_date):
    start = datetime.datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.datetime.strptime(end_date, "%d/%m/%Y")
    date_string_list = [(start + datetime.timedelta(days=x)).strftime("%d/%m/%Y") for x in range(0, (end-start).days + 1)]
    return date_string_list

# returns a date-string list containing every date related to days of week, from today() to end_date (dd/mm/yyyy)
def get_date_list_by_dow(days_of_week_list, end_date):
    start = datetime.datetime.strptime(datetime.date.today().strftime("%d/%m/%Y"), "%d/%m/%Y")
    end = datetime.datetime.strptime(end_date, "%d/%m/%Y")
    date_string_list = []
    date_string_list = [(start + datetime.timedelta(days=x)).strftime("%d/%m/%Y") for x in range(0, (end-start).days + 1) if convert_num((start + datetime.timedelta(days=x)).weekday()).lower() in days_of_week_list]
    return date_string_list

def get_end_of_academic_year():
    today = datetime.date.today().strftime("%d/%m/%Y")
    date = [int(key) for key in today.split('/')]
    # if month < 8 --> current year
    if date[1] < 8:
        return "31/08/" + str(date[2])
    return "31/08/" + str(date[2] + 1)


# accepts a dd/mm/yyyy date string and returns a yyyymmdd integer
def datestring_to_int(date_string):
    str_array = date_string.split('/')
    day = int(str_array[0])
    month = int(str_array[1])
    year = int(str_array[2])
    return year * 10000 + month * 100 + day

# accepts a yyyymmdd integer and returns a dd/mm/yyyy date string
def dateint_to_string(date_int):
    year = str(int(date_int / 10000))
    month = str(int((date_int % 10000)/100))
    day = str(int(date_int % 100))
    return day + '/' + month + '/' + year

def get_current_date_string():
    return datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")