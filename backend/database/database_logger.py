"""
    This module manage logs
"""
import sqlite3
import datetime

class DatabaseLogger:
    data_logs = "data_log.db"
    """
    This class manage logging
    """
    def __init__(self):
        pass

    @staticmethod
    def log_car_add_to_master_table(func):
        """
        Description: Function decorator for CarsDatabase.add_new_car_to_table;
        Creates a log in the backup_master_table table in the data_log.db
        database in the (make, model, year, vin, datetime, action_description)
        format
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
    def log_rating_added_to_rating_table(vin, rating, comment, date_time):
        """
        // Function description
        """

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
    def log_status_change(vin, status):
        """
        // Function description
        """

    @staticmethod
    def log_get_status_request(vin, status):
        """
        // Function description
        """

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
    def log_car_added_to_rented_table(vin, start_date, end_date):
        """
        // Function description
        """

    @staticmethod
    def log_car_removed_from_rented_table(vin):
        """
        // Function description
        """
