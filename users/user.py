class User:

    def __init__(self, name, charisma, light_shifts, heavy_shifts,
                 light_punitive_shifts, heavy_punitive_shifts, admonitions,
                 availability, forbidden_links):

        # Define the name of the user
        self.name = name
        # Quantify how much the user is appreciated by the community (range value: 0-10)
        # People with low values should never be together in a shift
        self.charisma = charisma
        # Define the number of light shifts of this user during the year (should be reset in August)
        # A light shift is a shift with less work to do with few users involved
        self.light_shifts = light_shifts
        # Define the number of heavy shifts of this user during the year (should be reset in August)
        # A heavy shift is a shift with much work to do with a lot of users involved
        self.heavy_shifts = heavy_shifts
        # Define the number of punitive light shifts
        self.light_punitive_shifts = light_punitive_shifts
        # Define the number of punitive heavy shifts
        self.heavy_punitive_shifts = heavy_punitive_shifts
        # Define the number of admonitions of this user
        self.admonitions = admonitions
        # Define the availability of the user during the month
        self.availability = availability
        # Define name of users which should not be linked
        self.forbidden_links = forbidden_links
