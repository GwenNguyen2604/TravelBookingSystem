import datetime
import time

class DatabaseLogger:
    def __init__(self):
        pass

    @staticmethod
    def log_car_add_to_master_table(make, model, year, vin):
        pass

    @staticmethod
    def log_rating_added_to_rating_table(vin, rating, comment, date_time):
        pass

    @staticmethod
    def log_rating_request(vin):
        pass

    @staticmethod
    def log_failed_rating_request(vin):
        pass

    @staticmethod
    def log_rental_price_request(vin):
        pass

    @staticmethod
    def log_rental_price_failed_request(vin):
        pass

    @staticmethod
    def log_rental_price_added(vin, price):
        pass

    @staticmethod
    def log_rental_price_fail_added(vin):
        pass

    @staticmethod
    def log_status_change(vin, status):
        pass

    @staticmethod
    def log_get_status_request(vin, status):
        pass

    @staticmethod
    def log_maintenance_table_add(vin):
        pass

    @staticmethod
    def log_maintenance_table_remove(vin, start_time, end_time, service_performed):
        pass

    @staticmethod
    def log_car_added_to_rented_table(vin, start_date, end_date):
        pass

    @staticmethod
    def log_car_removed_from_rented_table(vin):
        pass