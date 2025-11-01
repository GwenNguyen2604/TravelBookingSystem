"""
    This module manage logs
"""
import sqlite3
import datetime

class DatabaseLogger:
    """
    This class manage logging
    """
    data_logs = "data_log.db"
    
    def __init__(self):
        pass

    @staticmethod
    def log_car_add_to_master_table(func):
        """
        Description: Function decorator for CarsDatabase.add_new_car_to_table;
        Creates a log in the backup_master_table table in the data_log.db
        database in the (make, model, year, vin, datetime, action_description)
        format.
        """
        def wrapper(*args):
            logger = sqlite3.connect(DatabaseLogger.data_logs)

            logger.execute("""CREATE TABLE IF NOT EXISTS backup_master_table (
                           make TEXT,
                           model TEXT,
                           year INTEGER,
                           vin TEXT,
                           datetime TEXT,
                           action_description TEXT)
            """)

            log_time = datetime.datetime.now().isoformat()

            logger.execute("""INSERT INTO backup_master_table
                        (make, model, year, vin, datetime, action_description)
                           VALUES (?, ?, ?, ?, ?, ?)
            """, (*args, log_time, "Add new car to master table",))

            logger.commit()

            return func(*args)
        return wrapper
    
    @staticmethod
    def log_rating_added_to_rating_table(func):
        """
        Description: Function decorator for add_new_rating_and_comment in the
        CarsDatabase class. Creates a log in the rating_comment_table in the
        data_log.db database in the 
        (vin, rating, comment, date_time, action_description) format.
        """
        def wrapper(*args):
            logger = sqlite3.connect(DatabaseLogger.data_logs)

            logger.execute("""CREATE TABLE IF NOT EXISTS rating_comment_table (
                           vin TEXT,
                           rating TEXT,
                           comment TEXT,
                           datetime TEXT,
                           action_description TEXT
            )""")    

            log_time = datetime.datetime.now().isoformat()

            logger.execute("""INSERT INTO rating_comment_table 
            (vin, rating, comment, datetime, action_description) VALUES
            (?, ?, ?, ?, ?)""", (*args, log_time, "rating and comment added"))

            logger.commit()
            
            return func(*args)
        return wrapper  

    @staticmethod
    def log_rating_request(vin):
        """
        // Function description
        """

    @staticmethod
    def log_failed_rating_request(vin):
        """
        // Function description
        """

    @staticmethod
    def log_rental_price_request(vin):
        """
        // Function description
        """

    @staticmethod
    def log_rental_price_failed_request(vin):
        """
        // Function description
        """

    @staticmethod
    def log_rental_price_added(vin, price):
        """
        // Function description
        """

    @staticmethod
    def log_rental_price_fail_added(vin):
        """
        // Function description
        """

    @staticmethod
    def log_new_status_add(func):
        """
        Description: Function decorator for add_new_status_to_table in the
        CarsDatabase class. Creates a log in the backup_status_table table
        in the data_log.db database in the
        (vin, status, datetime, action_description) format.
        """
        def wrapper(*args):
            logger = sqlite3.connect(DatabaseLogger.data_logs)
            
            logger.execute(""" CREATE TABLE IF NOT EXISTS backup_status_table (
                           vin TEXT,
                           status TEXT,
                           datetime TEXT,
                           action_description TEXT
            )""")

            log_time = datetime.datetime.now().isoformat()

            logger.execute("""INSERT INTO backup_status_table
            (vin, status, datetime, action_description) VALUES
            (?, ?, ?, ?) """, (*args, log_time, "New status added to table"))

            logger.commit()

            return func(*args)
        return wrapper

    @staticmethod
    def log_status_change(func):
        """
        Description: Function decorator for set_status_to_table in the
        CarsDatabase class. Creates a log in the backup_status_table in
        the data_log.db database in the 
        (vin, status, datetime, action_description) format.
        """
        def wrapper(*args):
            logger = sqlite3.connect(DatabaseLogger.data_logs)

            logger.execute("""CREATE TABLE IF NOT EXISTS backup_status_table (
                           vin TEXT,
                           status TEXT,
                           datetime TEXT,
                           action_description TEXT
            )""")

            log_time = datetime.datetime.now().isoformat()

            logger.execute("""INSERT INTO backup_status_table
            (vin, status, datetime, action_description) VALUES
            (?, ?, ?, ?)""", (*args, log_time, "status changed"))

            logger.commit()

            return func(*args)
        return wrapper

    @staticmethod
    def log_get_status_request(func):
        """
        Description: Function decorator for get_status_from_table in the
        CarsDatabase class. Creates a log in the backup_status_table in the
        data_log.db database in the (vin, status, datetime, action_description)
        format.
        """
        def wrapper(*args):
            logger = sqlite3.connect(DatabaseLogger.data_logs)

            logger.execute("""CREATE TABLE IF NOT EXISTS backup_status_table (
                           vin TEXT,
                           status TEXT,
                           datetime TEXT,
                           action_description TEXT
            )""")

            log_time = datetime.datetime.now().isoformat()

            logger.execute("""INSERT INTO backup_status_table
            (vin, status, datetime, action_description) VALUES
            (?, ?, ?, ?)""", (*args, log_time, "status of vin requested"))

            logger.commit()

            return func(*args)
        return wrapper

    @staticmethod
    def log_maintenance_table_add(vin):
        """
        // Function description
        """

    @staticmethod
    def log_maintenance_table_remove(
        vin,
        start_time,
        end_time,
        service_performed
    ):
        """
        // Function description
        """

    @staticmethod
    def log_car_added_to_rented_table(func):
        """
        Description: Function decorator for add_car_to_rented_table
        in the DatabaseManager class. Creates a log in the 
        backup_rented_table in the data_log.db database in the
        (vin, start_date, end_date, datetime, action_description)
        format.
        """
        def wrapper(*args):
            logger = sqlite3.connect(DatabaseLogger.data_logs)

            logger.execute("""CREATE TABLE IF NOT EXISTS backup_rented_table (
                           vin TEXT,
                           start_time TEXT,
                           end_time TEXT,
                           datetime TEXT,
                           action_description TEXT
            )""")

            log_time = datetime.datetime.now().isoformat()

            logger.execute("""INSERT INTO backup_rented_table
            (vin, start_time, end_time, datetime, action_description) VALUES
            (?, ?, ?, ?, ?)""", (*args, log_time, "Car added to rented table"))

            logger.commit()

            return func(*args)
        return wrapper

    @staticmethod
    def log_car_removed_from_rented_table(func):
        """
        Description: Function decorator for remove_car_from_rented_table
        in the DatabaseManager class. Creates a log in the rented_table
        in the data_log.db database in the (vin, datetime, action_description)
        format.
        """
        def wrapper(*args):
            logger = sqlite3.connect(DatabaseLogger.data_logs)

            logger.execute("""CREATE NEW TABLE IF NOT EXISTS backup_rented_table (
                            vin TEXT,
                            start_time TEXT,
                            end_time TEXT,
                            datetime TEXT,
                            action_description TEXT
            )""")

            log_time = datetime.datetime.now().isoformat()

            logger.execute("""INSERT INTO backup_rented_table 
            (vin, datetime, action_description) VALUES 
            (?, ?, ?)""", (*args, log_time, "Car removed from rented table"))

            logger.commit()
            
            return func(*args)
        return wrapper
