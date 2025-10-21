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
    def add_new_car_to_table(make, model, year, vin):
        con = sqlite3.connect(CarsDatabase.database)

        database_logger.DatabaseLogger.LogCarAddToMasterTable(make, model, year, vin)

        con.execute("CREATE TABLE IF NOT EXISTS master_table (make TEXT, model TEXT, year INTEGER, vin TEXT)")

        con.execute("INSERT INTO cars (make, model, year, vin) VALUES (?, ?, ?, ?)", (make, model, year, vin,))

        con.commit()
    
    # Description: Gets all car data from the master table in the 'cars.db' database and returns a sqlite object
    @staticmethod
    def get_all_cars_from_master_table():
        con = sqlite3.connect(CarsDatabase.database)

        data = con.execute("SELECT * FROM master_table")

        con.commit()

        return data

    # Description: Returns true if the database exists, otherwise returns false
    @staticmethod
    def check_if_database_exists():
        return os.path.exists(CarsDatabase.database)

    # *** RATING MANAGER ***

    # Description: Returns a sqlite object containing all rating data given a vin; Returns nothing if there are no ratings
    @staticmethod
    def get_all_ratings(vin):
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
    def add_new_rating_and_comment(vin, rating, comment):
        con = sqlite3.connect(CarsDatabase.database)

        date_time = datetime.date.fromtimestamp(time.time()).isoformat()

        con.execute("CREATE TABLE IF NOT EXISTS ?_rating_comment_table (rating TEXT, comment TEXT, datetime TEXT)", (vin,))

        con.execute("INSERT INTO ?_rating_comment_table (rating, comment, datetime) VALUES (?, ?, ?)", (vin, rating, comment, date_time,))

        database_logger.DatabaseLogger.LogRatingAddedToRatingTable(vin, rating, comment, date_time)

        con.commit()

    # *** RENTAL PRICE MANAGER ***

    # Description: Adds a rental price to a vin if the vin doesn't exist in the table
    @staticmethod
    def add_rental_price_to_table(vin, price):
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("CREATE TABLE IF NOT EXISTS rental_price_table (vin TEXT, rental_price TEXT)")

        exists = con.execute("SELECT * FROM rental_price_table WHERE vin = ?", (vin,))

        if (exists.arraysize != 0): 
            database_logger.DatabaseLogger.LogRentalPriceFailAdded(vin)
            return

        con.execute("INSERT INTO rental_price_table (vin, rental_price) VALUES (?, ?)", (vin, price,))

        database_logger.DatabaseLogger.LogRentalPriceAdded(vin, price)

        con.commit()

    # Description: Gets a rental price from the table given a vin number; Returns nothing if the vin doesn't exist
    @staticmethod
    def get_rental_price_from_table(vin):
        con = sqlite3.connect(CarsDatabase.database)

        exists = con.execute("SELECT * FROM rental_price_table WHERE vin = ?", (vin,))

        if (exists.arraysize == 0): return

        price = con.execute("SELECT rental_price FROM rental_price_table WHERE vin = ?", (vin,))

        con.commit()

        return price

    # Description: Gets all rental prices and vins from the rental_price_table table as a sqlite object
    @staticmethod
    def get_all_rental_prices_from_table():
        con = sqlite3.connect(CarsDatabase.database)

        allPrices = con.execute("SELECT * FROM rental_price_table")

        con.commit()

        return allPrices

    # Description: Sets a new price to an existing vin in the rental_price_table table. Returns if the vin doesn't exist
    @staticmethod
    def update_rental_price_in_table(vin, new_price):
        con = sqlite3.connect(CarsDatabase.database)

        exists = con.execute("SELECT * FROM rental_price_table WHERE vin = ?", (vin,))

        if (exists.arraysize == 0): return

        con.execute("UPDATE rental_price_table SET rental_price = ? WHERE vin = ?", (new_price, vin,))

        con.commit()

    #STATUS MANAGER
    @staticmethod
    def set_status_to_table(vin, status):
        pass

    @staticmethod
    def get_status_from_table(vin):
        pass

    #RENTED CAR MANAGER
    @staticmethod
    def add_car_to_rented_table(vin, start_time, end_time):
        pass

    @staticmethod
    def remove_car_from_rented_table(vin):
        pass

    #MAINTENANCE MANAGER
    @staticmethod
    def move_car_to_maintenance_table(vin):
        pass

    @staticmethod
    def set_time_in_maintenance(vin, time_in):
        pass

    @staticmethod
    def set_time_out_maintenance(vin, time_out):
        pass

    @staticmethod
    def set_service_performed_maintenance(vin, service_performed):
        pass

    @staticmethod
    def write_to_maintenance_log_table(vin, time_in, time_out, service_performed):
        pass

