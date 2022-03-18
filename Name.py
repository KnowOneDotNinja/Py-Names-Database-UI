from Database import Database


class Name:
    # Create Name object parameters
    __name = ""
    __gender = ""
    __year = 0
    __rank = 0

    # Initialize
    def __init__(self, name, gender, year, rank):
        self.__name = name
        self.__gender = gender
        self.__year = year
        self.__rank = rank

    # Getters for parameters
    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_year(self):
        return self.__year

    def get_rank(self):
        return self.__rank

    # Method to get list from database using user input
    @staticmethod
    def fetch_names(year, gender):
        return Database.readNames(year, gender)


# This class handles the info for the 'gender' combobox
class NameGender:
    ALL_GENDERS = '-- All Genders --'

    def __init__(self, gender):
        self._gender = gender

    def get_gender(self):
        return self._gender

    @staticmethod
    def fetch_genders():
        return Database.get_genders()


# This class handles the info for the 'years' combobox
class NameYear:
    ALL_YEARS = '-- All Years --'

    def __init__(self, year):
        self._year = year

    def get_year(self):
        return self._year

    @staticmethod
    def fetch_years():
        return Database.get_years()
