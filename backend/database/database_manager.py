"""
    This module manages database
"""
import sqlite3
import os
import datetime
import database_logger


class CarsDatabase:
    """
    This class is the car database class
    """

    database = 'cars.db'

    def __init__(self):
        pass

    # *** MASTER TABLE ***

    @database_logger.DatabaseLogger.log_car_add_to_master_table
    @staticmethod
    def add_new_car_to_table(make, model, year, vin):
        """
        Description: Adds a car to the master table in the 'cars.db' database
        """
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("""
                        CREATE TABLE IF NOT EXISTS master_table (
                            make TEXT,
                            model TEXT,
                            year INTEGER,
                            vin TEXT)
                    """)

        con.execute("""
                        INSERT INTO master_table (make, model, year, vin)
                        VALUES (?, ?, ?, ?)
                    """, (make, model, year, vin,))

        con.commit()

    @staticmethod
    def get_all_cars_from_master_table():
        """
        Description: Gets all car data from the master table in the
                     'cars.db' database
                     returns a sqlite object
        """
        con = sqlite3.connect(CarsDatabase.database)

        data = con.execute("SELECT * FROM master_table")

        con.commit()

        return data

    @staticmethod
    def check_if_database_exists():
        """
        Description: Returns true if the database exists,
                     otherwise returns false
        """
        return os.path.exists(CarsDatabase.database)
    
    # *** RATING MANAGER ***

    @staticmethod
    def get_all_ratings(vin):
        """
        Description: returns a sqlite object containing all rating data
                     given a vin;
                     Returns nothing if there are no ratings
        """
        con = sqlite3.connect(CarsDatabase.database)

        database_logger.DatabaseLogger.log_rating_request(vin)

        exists = con.execute("""
                                SELECT *
                                FROM rating_master WHERE vin = ?
                             """, (vin,))

        if exists.arraysize == 0:
            database_logger.DatabaseLogger.log_failed_rating_request(vin)
            return None

        rating_data = con.execute("""
                                    SELECT *
                                    FROM ?_rating_comment_table
                                  """, (vin,))

        con.commit()

        return rating_data

    @staticmethod
    def add_new_rating_and_comment(vin, rating, comment):
        """
        Description: Adds a rating and a comment to a unique table for the vin;
                     Creates a new table if the vin doesn't exist
                     in the rating_master table
        """
        con = sqlite3.connect(CarsDatabase.database)

        date_time = datetime.datetime.now().isoformat()

        con.execute("""
                        CREATE TABLE IF NOT EXISTS ?_rating_comment_table (
                            rating TEXT,
                            comment TEXT,
                            datetime TEXT
                        )
                    """, (vin,))

        con.execute("""
                        INSERT INTO ?_rating_comment_table (
                            rating,
                            comment,
                            datetime
                        )
                        VALUES (?, ?, ?)
                    """, (vin, rating, comment, date_time,))

        database_logger.DatabaseLogger.log_rating_added_to_rating_table(
            vin, rating, comment, date_time
        )

        con.commit()
    # *** RENTAL PRICE MANAGER ***

    @staticmethod
    def add_rental_price_to_table(vin, price):
        """
        Description: Adds a rental price to a vin
                     if the vin doesn't exist in the table
        """
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("""
                        CREATE TABLE IF NOT EXISTS rental_price_table (
                            vin TEXT,
                            rental_price TEXT
                        )
                    """)

        exists = con.execute("""
                                SELECT *
                                FROM rental_price_table
                                WHERE vin = ?
                             """, (vin,))

        if exists.arraysize != 0:
            database_logger.DatabaseLogger.log_rental_price_fail_added(vin)
            return

        con.execute("""
                        INSERT INTO rental_price_table (
                            vin,
                            rental_price
                        )
                        VALUES (?, ?)
                    """, (vin, price,))

        database_logger.DatabaseLogger.log_rental_price_added(vin, price)

        con.commit()

    @staticmethod
    def get_rental_price_from_table(vin):
        """
        Description: Gets a rental price from the table given a vin number;
                     Returns nothing if the vin doesn't exist
        """
        con = sqlite3.connect(CarsDatabase.database)

        exists = con.execute("""
                                SELECT *
                                FROM rental_price_table
                                WHERE vin = ?
                             """, (vin,))

        if exists.arraysize == 0:
            return None

        price = con.execute("""
                                SELECT rental_price
                                FROM rental_price_table
                                WHERE vin = ?
                            """, (vin,))

        con.commit()

        return price

    @staticmethod
    def get_all_rental_prices_from_table():
        """
        Description: Gets all rental prices and vins from the
                     rental_price_table as a sqlite object
        """
        con = sqlite3.connect(CarsDatabase.database)

        all_prices = con.execute("SELECT * FROM rental_price_table")

        con.commit()

        return all_prices

    @staticmethod
    def update_rental_price_in_table(vin, new_price):
        """
        Description: Sets a new price to an existing vin in the
                     rental_price_table. Returns if the vin doesn't exist
        """
        con = sqlite3.connect(CarsDatabase.database)

        exists = con.execute("""
                                SELECT *
                                FROM rental_price_table
                                WHERE vin = ?
                             """, (vin,))

        if exists.arraysize == 0:
            return

        con.execute("""
                        UPDATE rental_price_table
                        SET rental_price = ?
                        WHERE vin = ?
                    """, (new_price, vin,))

        con.commit()

    # STATUS MANAGER
    @database_logger.DatabaseLogger.log_new_status_add
    @staticmethod
    def add_new_status_to_table(vin, status):
        """
        Description: Adds a new vin to the table and sets the status;
        Returns if the vin already exists in the table
        """
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("""CREATE TABLE IF NOT EXISTS status_table (
                    vin TEXT,
                    status TEXT
        )""")

        exists = con.execute("""SELECT * FROM status_table WHERE vin = ?"""
        , (vin,))
        
        if (exists.arraysize != 0): return

        con.execute("""INSERT INTO status_table (vin, status) VALUES (?, ?)
        """, (vin, status,))

        con.commit()

    @database_logger.DatabaseLogger.log_status_change
    @staticmethod
    def set_status_to_table(vin, status):
        """
        Description: Sets the status of a vin in the status table;
        Does nothing if the vin doesn't exist
        """
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("""CREATE TABLE IF NOT EXISTS status_table (
                    vin TEXT,
                    status TEXT
        )""")

        con.execute("""UPDATE status_table SET status = ? WHERE vin = ?
        """, (status, vin,))

        con.commit()

    @database_logger.DatabaseLogger.log_get_status_request
    @staticmethod
    def get_status_from_table(vin):
        """
        Description: Gets the status of a vin from the status table;
        Returns a sqlite object containing the status
        """
        con = sqlite3.connect(CarsDatabase.database)

        status = con.execute("SELECT status FROM status_table WHERE vin = ?"
        ,(vin,))

        con.commit()

        return status
    
    # RENTED CAR MANAGER
    @staticmethod
    def add_car_to_rented_table(vin, start_time, end_time):
        """
        // Function description
        """

    @staticmethod
    def remove_car_from_rented_table(vin):
        """
        // Function description
        """

    # MAINTENANCE MANAGER
    @staticmethod
    def move_car_to_maintenance_table(vin):
        """
        // Function description
        """

    @staticmethod
    def set_time_in_maintenance(vin, time_in):
        """
        // Function description
        """

    @staticmethod
    def set_time_out_maintenance(vin, time_out):
        """
        // Function description
        """

    @staticmethod
    def set_service_performed_maintenance(vin, service_performed):
        """
        // Function description
        """

    @staticmethod
    def write_to_maintenance_log_table(
        vin,
        time_in,
        time_out,
        service_performed
    ):
        """
        // Function description
        """
