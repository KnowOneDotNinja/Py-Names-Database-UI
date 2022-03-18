import pyodbc


class Database:
    __connection = None

    # Establish connection to database
    @classmethod
    def connect(cls):
        if cls.__connection is None:
            server = 'tcp:cisdbss.pcc.edu'
            database = 'NAMES'
            username = '275student'
            password = '275student'
            cls.__connection = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=' + server
                + ';DATABASE=' + database
                + ';UID=' + username + ';PWD=' + password
            )

    @classmethod
    def get_genders(cls):
        from Name import NameGender

        # Select only the gender column from database table
        sql = '''
        SELECT DISTINCT Gender
        FROM all_data;
        '''

        # Establish connection and create cursor
        cls.connect()
        cursor = cls.__connection.cursor()

        # Make SQL call to retrieve list of available genders
        cursor.execute(sql)
        genders = []
        gender = cursor.fetchone()

        while gender:
            genders.append(NameGender(gender[0]))
            gender = cursor.fetchone()

        return genders

    @classmethod
    def get_years(cls):
        from Name import NameYear

        # Select only the year column from database table
        sql = '''
        SELECT DISTINCT Year
        FROM all_data;
        '''

        # Establish connection and create cursor
        cls.connect()
        cursor = cls.__connection.cursor()

        # Make SQL call to retrieve list of available years
        cursor.execute(sql)
        years = []
        year = cursor.fetchone()

        while year:
            years.append(NameYear(year[0]))
            year = cursor.fetchone()

        return years

    @classmethod
    def readNames(cls, year, gender):
        from Name import NameGender, NameYear
        # Establish connection and create cursor
        cls.connect()
        myConnection = cls.__connection
        cursor = myConnection.cursor()

        # Create call to database
        # I chose to include 'Total > 1' so that my concatenations both started with AND
        sql = '''
        SELECT DISTINCT TOP 25 Name, Gender, Year, Rank
        FROM all_data
        WHERE Total > 1
        '''

        # Contingencies for no value selected
        if year != NameYear.ALL_YEARS:
            sql += '''
            AND Year = ?
            '''
        if gender != NameGender.ALL_GENDERS:
            sql += '''
            AND Gender = ?
            '''
        sql += '''
        ORDER BY Rank ASC;
        '''

        # Create an object to return to Name.fetch_names()
        if year != NameYear.ALL_YEARS and gender != NameGender.ALL_GENDERS:
            names = cursor.execute(sql, year, gender)
        elif year != NameYear.ALL_YEARS:
            names = cursor.execute(sql, year)
        elif gender != NameGender.ALL_GENDERS:
            names = cursor.execute(sql, gender)
        else:
            names = cursor.execute(sql)

        # Return object to Name.fetch_names()
        return names
