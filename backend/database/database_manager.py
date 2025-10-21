import sqlite3
import os

DB_FILE = "car_Rental.db"
CARS_TABLE = "cars"
MAINT_TABLE = "maint_cars"
VALID_COLUMNS = {"brand", "model", "year", "vin"}

# Name: CheckIfDatabaseExists
# Description: Returns true if the database exists, false otherwise
def CheckIfDatabaseExists():
    return os.path.exists(DB_FILE)


# Name: WriteNewCarToTable
# Description: Creates a new car entry to the table in the database
def WriteNewCarToTable(brand_name, model_name, model_year, car_vin):
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


# Name: GetAllCarsFromTable
# Description: Gets the data of the cars in the database
def GetAllCarsFromTable():
    con = sqlite3.connect(DB_FILE)

    # List of tables
    tables = [(CARS_TABLE, "*** cars table ***"),
              (MAINT_TABLE, "\n*** maint_cars table ***")]
    car_data = {};

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


# Name: MoveCarToMaintenanceTable
# Description: Moves a car from the cars table to the maintenance table
def MoveCarToMaintenanceTable(car_vin):
    MoveCarBetweenTablesUtil(CARS_TABLE, MAINT_TABLE, car_vin)


# Name: MoveMaintCarToCarsTable
# Description: Moves a car from the maintenance table to the cars table
def MoveMaintCarToCarsTable(car_vin):
    MoveCarBetweenTablesUtil(MAINT_TABLE, CARS_TABLE, car_vin)


# Name: GetAllVinsGivenBrand
# Description: Returns a sql object of all vins given a brand parameter from the cars table
def GetAllVinsGivenBrand(brand_name):
    return GetAllVinsWithFilterUtil("brand", brand_name)


# Name: GetAllVinsGivenModel
# Description: Returns a sql object of all vins given a model parameter from the cars table
def GetAllVinsGivenModel(model_name):
    return GetAllVinsWithFilterUtil("model", model_name)


# Name: GetAllVinsGivenYear
# Description: Returns a sql object of all vins given a year parameter from the cars table
def GetAllVinsGivenYear(year_num):
    return GetAllVinsWithFilterUtil("year", year_num)


# Name: GetAllCarDataGivenBrand
# Description: Returns a sql object of all car data given the brand from the cars table
def GetAllCarDataGivenBrand(brand_name):
    return GetAllCarsWithFilterUtil("brand", brand_name)


# Name: GetAllCarDataGivenModel
# Description: Returns a sql object of all car data given the model from the cars table
def GetAllCarDataGivenModel(model_name):
    return GetAllCarsWithFilterUtil("model", model_name)


# Name: GetAllCarDataGivenYear
def GetAllCarDataGivenYear(year_num):
    return GetAllCarsWithFilterUtil("year", year_num)


# Name: MoveCarBetweenTablesUtil
# Description: Utillity function to move a car entry between tables. Used by
#             MoveCarToMaintenanceTable and MoveMaintCarToCarsTable
def MoveCarBetweenTablesUtil(source_table, dest_table, car_vin):
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


# Name: GetAllVinsWithFilterUtil
# Description: Utillity function to get all VINs data given a filtering parameter
#              Current Filters: brand_name, model_name, year
def GetAllVinsWithFilterUtil(filter_field, filter_value):
    con = sqlite3.connect(DB_FILE)
    all_cars = con.execute(f"SELECT vin FROM {CARS_TABLE} WHERE {filter_field} = ?",
                           (filter_value,))
    con.commit()
    return all_cars


# Name: GetAllCarsWithFilterUtil
# Description: Utillity function to get all car data given a filtering parameter
#              Current Filters: brand_name, model_name, year
def GetAllCarsWithFilterUtil(filter_field, filter_value):
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
