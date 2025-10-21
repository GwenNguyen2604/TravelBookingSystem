"""
    This module manages database
"""
import sqlite3
import os

DB_FILE = "car_Rental.db"
CARS_TABLE = "cars"
MAINT_TABLE = "maint_cars"
VALID_COLUMNS = {"brand", "model", "year", "vin"}

def check_if_database_exists():
    """
    Check if the database exists

    Returns:
        bool: if the database exists
    """
    return os.path.exists(DB_FILE)


def write_new_car_to_table(brand_name, model_name, model_year, car_vin):
    """
    Append new car entry to the cars table

    Args:
        brand_name (string) : Brand name of the car
        model_name (string) : Car's model name
        model_year (string?) : Model year
        car_vin (string?) : Car VIN
    """

    # create the values
    car_entries = (brand_name, model_name, model_year, car_vin)
    # Build the column
    col_str = ", ".join(sorted(VALID_COLUMNS))  # sorted ensures consistent order

    con = sqlite3.connect(DB_FILE)

    # Create table if missing
    con.execute(f"""CREATE TABLE IF NOT EXISTS {CARS_TABLE} (
                        brand TEXT,
                        model TEXT,
                        year INTEGER,
                        vin TEXT PRIMARY KEY
                )""")
    # Insert new car
    con.execute(
        f"INSERT INTO {CARS_TABLE} ({col_str}) VALUES (?, ?, ?, ?)",
        car_entries
    )
    con.commit()


def get_all_cars_from_table():
    """
    Print out all cars entries from teh cars table and maint_cars table

    Returns:
        list: All car entries from only the cars table
    """

    con = sqlite3.connect(DB_FILE)

    # List of tables
    tables = [(CARS_TABLE, "*** cars table ***"),
              (MAINT_TABLE, "\n*** maint_cars table ***")]
    car_data = {}

    # Iterate through both maint and cars tables to print.
    # Return only data from cars table
    for table_name, header in tables:
        print(header)
        rows = con.execute(f"SELECT * FROM {table_name}").fetchall()
        for row in rows:
            print(row)
        if table_name == CARS_TABLE:
            car_data[table_name] = rows

    con.commit()
    return car_data


def move_car_to_maintenance_table(car_vin):
    """
    Move a specified car entry to the maint table

    Args:
        car_vin (string): The car VIN
    """
    move_car_between_tables_util(CARS_TABLE, MAINT_TABLE, car_vin)


def move_maint_car_to_cars_table(car_vin):
    """
    Move a specified car entry fromt the cars table to the maint table

    Args:
        car_vin (string): The car VIN
    """
    move_car_between_tables_util(MAINT_TABLE, CARS_TABLE, car_vin)


def get_all_vins_given_brand(brand_name):
    """
    Get a sql object of all vins given the car's brand parameter from the cars table

    Args:
        brand_name (string): The car's brand

    Returns:
        the sql object of all vins
    """
    return get_all_vins_with_filter_util("brand", brand_name)


def get_all_vins_given_model(model_name):
    """
    Get a sql object of all vins given a model parameter from the cars table

    Args:
        model_name (string): The car's model name

    Returns:
        the sql object of all vins
    """
    return get_all_vins_with_filter_util("model", model_name)


def get_all_vins_given_year(year_num):
    """
    Get a sql object of all vins given a year parameter from the cars table

    Args:
        year_num (string): The car's year

    Returns:
        the sql object of all vins
    """
    return get_all_vins_with_filter_util("year", year_num)


def get_all_car_data_given_brand(brand_name):
    """
    Get a sql object of all car data given the brand from the cars table

    Args:
        brand_name (string): The car's brand name

    Returns:
        the sql object of all car data
    """
    return get_all_cars_with_filter_util("brand", brand_name)


def get_all_car_data_given_model(model_name):
    """
    Get a sql object of all car data given the model from the cars table

    Args:
        model_name (string): The car's model name

    Returns:
        the sql object of all car data
    """
    return get_all_cars_with_filter_util("model", model_name)


def get_all_car_data_given_year(year_num):
    """
    Get a sql object of all car data given the year from the cars table

    Args:
        year_num (string): The car's year

    Returns:
        the sql object of all car data
    """
    return get_all_cars_with_filter_util("year", year_num)


def move_car_between_tables_util(source_table, dest_table, car_vin):
    """
    Utillity function to move a car entry between tables.
    Used by MoveCarToMaintenanceTable and MoveMaintCarToCarsTable

    Args:
        source_table (table): The table where the data is from
        dest_table (table): The table where it is being moved to
        car_vin (string): car's VIN
    """

    con = sqlite3.connect(DB_FILE)

    #check if the car exists in the source table
    check = con.execute(f"SELECT vin FROM {source_table} WHERE vin = ?", (car_vin,))

    if check.fetchall() == []: return

    #Creates destination table if it doesn't exist
    con.execute(f"""CREATE TABLE IF NOT EXISTS {dest_table} (
                brand TEXT, model TEXT, year INTEGER, vin TEXT
                )""")

    # Move car entry betwen source and destination table
    con.execute(f"INSERT INTO {dest_table} SELECT * FROM {source_table} WHERE vin = ?",
                (car_vin,))
    con.execute(f"DELETE FROM {source_table} WHERE vin = ?", (car_vin,))
    con.commit()



def get_all_vins_with_filter_util(filter_field, filter_value):
    """
    Utillity function to get all VINs data given a filtering parameter
    Current Filters: brand_name, model_name, year

    Args:
        filter_field (string): The filtered field
        filter_value (string): the value filtered

    Returns:
        the sql object of all VINs data
    """

    con = sqlite3.connect(DB_FILE)
    all_cars = con.execute(f"SELECT vin FROM {CARS_TABLE} WHERE {filter_field} = ?",
                           (filter_value,))
    con.commit()
    return all_cars


def get_all_cars_with_filter_util(filter_field, filter_value):
    """
    Utillity function to get all car data given a filtering parameter
    Current Filters: brand_name, model_name, year

    Args:
        filter_field (string): The filtered field
        filter_value (string): the value filtered

    Returns:
        the sql object of all car data
    """

    con = sqlite3.connect(DB_FILE)
    allCars = con.execute(f"SELECT * FROM {CARS_TABLE} WHERE {filter_field} = ?",
                          (filter_value,))
    con.commit()
    return allCars


# Name: AddColumnToCarsTable
# Description: Adds a vin column, data type TEXT to the cars table
#Note: Run this function if the database has not been updated with a new column for the vin
#def AddColumnToCarsTable():
    #con = sqlite3.connect(DB_FILE)

    #con.execute("ALTER TABLE cars ADD vin TEXT")

    #con.commit()
