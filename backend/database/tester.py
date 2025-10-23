"""
This file is to solely test the functions in the database management modules.
Do not import this file anywhere unless to test the database management modules.
Do not call the functions contained within this file elsewhere outside of this file.
"""
import sqlite3
import database_manager
# import database_duplicator

cars_database = "cars.db"
logger_database = "data_log.db"

# Test the output of adding a new car to the database
def test_add_new_car():
    database_manager.CarsDatabase.add_new_car_to_table("Toyota", "Camry", 2009, "4GC1CYC84DF143936")

    # Output the car in the cars database
    con = sqlite3.connect(cars_database)

    car_data = con.execute("SELECT * FROM master_table")

    car_data = car_data.fetchall()

    for data in car_data: print(data)

    con.commit()

    logger = sqlite3.connect(logger_database)

    log_data = logger.execute("SELECT * FROM backup_master_table")

    log_data = log_data.fetchall()

    for data in log_data: print(data)

    logger.commit()

def test_add_status():
    database_manager.CarsDatabase.add_new_status_to_table("5AC1CYC84DF143936")

    database_manager.CarsDatabase.add_new_status_to_table("5AC1CYC84DF143936", "MAINTENANCE")

    con = sqlite3.connect(cars_database)

    car_data = con.execute("SELECT * FROM master_table")

    car_data = car_data.fetchall()

    for data in car_data: print(data)

    con.commit()

    logger = sqlite3.connect(logger_database)

    log_data = logger.execute("SELECT * FROM backup_status_table")

    log_data = log_data.fetchall()

    for data in log_data: print(data)

    logger.commit()
# test_add_new_car()
test_add_status()

