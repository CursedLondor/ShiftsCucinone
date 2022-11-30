class User:

    def __init__(self, name, charisma, light_shifts, heavy_shifts, hood_shifts,
                 light_punitive_shifts, heavy_punitive_shifts,
                 hood_punitive_shifts, admonitions, remaining_admonitions, availability, forbidden_links):

        # Define the name of the user
        self.name = name
        # Quantify how much the user is appreciated by the community (range value: 0-10)
        # People with low values should never be together in a shift
        self.charisma = int(charisma)
        # Define the number of light shifts of this user during the year (should be reset in August)
        # A light shift is a shift with less work to do with few users involved
        self.light_shifts = int(light_shifts)
        # Define the number of heavy shifts of this user during the year (should be reset in August)
        # A heavy shift is a shift with much work to do with a lot of users involved
        self.heavy_shifts = int(heavy_shifts)
        # Define the number of hood shifts (introduced in Oct 2022)
        self.hood_shifts = int(hood_shifts)
        # Define the number of punitive light shifts
        self.light_punitive_shifts = int(light_punitive_shifts)
        # Define the number of punitive heavy shifts
        self.heavy_punitive_shifts = int(heavy_punitive_shifts)
        # Define the number of hood punitive shifts
        self.hood_punitive_shifts = int(hood_punitive_shifts)
        # Define the TOTAL number of admonitions of this user
        self.admonitions = int(admonitions)
        # Define the number of admonition the users hasn't discount yet
        self.remaining_admonitions = int(remaining_admonitions)
        # Define the dates where the user is NOT available during the month
        # [it is an integer array of numeric dates YYYYMMDD]
        if(availability):
            pattern = availability.split(";")
            self.availability = [int(numeric_date) for numeric_date in pattern]
        else:
            self.availability = []
        # Define name of users which should not be linked
        self.forbidden_links = forbidden_links
