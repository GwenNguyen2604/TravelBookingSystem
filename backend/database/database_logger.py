import datetime
import time

class DatabaseLogger:
    def __init__(self):
        pass

    @staticmethod
    def LogCarAddToMasterTable(make, model, year, vin):
        pass

    @staticmethod
    def LogRatingAddedToRatingTable(vin, rating, comment, date_time):
        pass

    @staticmethod
    def LogRatingRequest(vin):
        pass

    @staticmethod
    def LogFailedRatingRequest(vin):
        pass

    @staticmethod
    def LogRentalPriceRequest(vin):
        pass

    @staticmethod
    def LogRentalPriceAdded(vin, price):
        pass

    @staticmethod
    def LogStatusChange(vin, status):
        pass

    @staticmethod
    def LogGetStatusRequest(vin, status):
        pass

    @staticmethod
    def LogMaintenanceTableAdd(vin):
        pass

    @staticmethod
    def LogMaintenanceTableRemove(vin, start_time, end_time, service_performed):
        pass

    @staticmethod
    def LogCarAddedToRentedTable(vin, start_date, end_date):
        pass

    @staticmethod
    def LogCarRemovedFromRentedTable(vin):
        pass