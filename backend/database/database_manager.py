import sqlite3
import os
import database_logger
import datetime
import time

class CarsDatabase:
    database = 'cars.db'

    def __init__(self):
        pass

    # *** MASTER TABLE ***

    # Description: Adds a car to the master table in the 'cars.db' database
    @staticmethod
    def AddNewCarToTable(make, model, year, vin):
        con = sqlite3.connect(CarsDatabase.database)

        database_logger.DatabaseLogger.LogCarAddToMasterTable(make, model, year, vin)

        con.execute("CREATE TABLE IF NOT EXISTS master_table (make TEXT, model TEXT, year INTEGER, vin TEXT)")

        con.execute("INSERT INTO cars (make, model, year, vin) VALUES (?, ?, ?, ?)", (make, model, year, vin,))

        con.commit()
    
    # Description: Gets all car data from the master table in the 'cars.db' database and returns a sqlite object
    @staticmethod
    def GetAllCarsFromMasterTable():
        con = sqlite3.connect(CarsDatabase.database)

        data = con.execute("SELECT * FROM master_table")

        con.commit()

        return data

    # Description: Returns true if the database exists, otherwise returns false
    @staticmethod
    def CheckIfDatabaseExists():
        return os.path.exists(CarsDatabase.database)

    # *** RATING MANAGER ***

    # Description: Returns a sqlite object containing all rating data given a vin; Returns nothing if there are no ratings
    @staticmethod
    def GetAllRatings(vin):
        con = sqlite3.connect(CarsDatabase.database)

        database_logger.DatabaseLogger.LogRatingRequest(vin)

        exists = con.execute("SELECT * FROM rating_master WHERE vin = ?", (vin,))

        if (exists.arraysize == 0): 
            database_logger.DatabaseLogger.LogFailedRatingRequest(vin)
            return

        ratingData = con.execute("SELECT * FROM ?_rating_comment_table", (vin,))

        con.commit()

        return ratingData

    # Description: Adds a rating and a comment to a unique table for the vin; Creates a new table if the vin doesn't exist in the rating_master table
    @staticmethod
    def AddNewRatingAndComment(vin, rating, comment):
        con = sqlite3.connect(CarsDatabase.database)

        date_time = datetime.date.fromtimestamp(time.time()).isoformat()

        con.execute("CREATE TABLE IF NOT EXISTS ?_rating_comment_table (rating TEXT, comment TEXT, datetime TEXT)", (vin,))

        con.execute("INSERT INTO ?_rating_comment_table (rating, comment, datetime) VALUES (?, ?, ?)", (vin, rating, comment, date_time,))

        database_logger.DatabaseLogger.LogRatingAddedToRatingTable(vin, rating, comment, date_time)

        con.commit()

    # *** RENTAL PRICE MANAGER ***

    # Description: Adds a rental price to a vin if the vin doesn't exist in the table
    @staticmethod
    def AddRentalPriceToTable(vin, price):
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("CREATE TABLE IF NOT EXISTS rental_price_table (vin TEXT, rental_price TEXT)")

        exists = con.execute("SELECT * FROM rental_price_table WHERE vin = ?", (vin,))

        if (exists.arraysize != 0): return

        con.execute("INSERT INTO rental_price_table (vin, rental_price) VALUES (?, ?)", (vin, price,))

        con.commit()

    # Description: Gets a rental price from the table given a vin number; Returns nothing if the vin doesn't exist
    @staticmethod
    def GetRentalPriceFromTable(vin):
        con = sqlite3.connect(CarsDatabase.database)

        exists = con.execute("SELECT * FROM rental_price_table WHERE vin = ?", (vin,))

        if (exists.arraysize == 0): return

        price = con.execute("SELECT rental_price FROM rental_price_table WHERE vin = ?", (vin,))

        con.commit()

        return price

    # Description: Gets all rental prices and vins from the rental_price_table table as a sqlite object
    @staticmethod
    def GetAllRentalPricesFromTable():
        pass

    @staticmethod
    def UpdateRentalPriceInTable(vin, new_price):
        pass

    #STATUS MANAGER
    @staticmethod
    def SetStatusToTable(vin, status):
        pass

    @staticmethod
    def GetStatusFromTable(vin):
        pass

    #RENTED CAR MANAGER
    @staticmethod
    def AddCarToRentedTable(vin, start_time, end_time):
        pass

    @staticmethod
    def RemoveCarFromRentedTable(vin):
        pass

    #MAINTENANCE MANAGER
    @staticmethod
    def MoveCarToMaintenanceTable(vin):
        pass

    @staticmethod
    def SetTimeInMaintenance(vin, time_in):
        pass

    @staticmethod
    def SetTimeOutMaintenance(vin, time_out):
        pass

    @staticmethod
    def SetServicePerformedMaintenance(vin, service_performed):
        pass

    @staticmethod
    def WriteToMaintenanceLogTable(vin, time_in, time_out, service_performed):
        pass

