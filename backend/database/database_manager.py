import sqlite3
import os

#Name: CheckIfDatabaseExists
#Description: Returns true if the database exists, false otherwise
def CheckIfDatabaseExists():
    return os.path.exists('car_Rental.db')

#Name: WriteNewCarToTable
#Description: Creates a new car entry to the table in the database
def WriteNewCarToTable(brand_name, model_name, model_year, car_vin):
    con = sqlite3.connect('car_Rental.db')

    con.execute("INSERT INTO cars (brand, model, year, vin) VALUES (?, ?, ?, ?)", (brand_name, model_name, model_year, car_vin))

    con.commit()

#Name: GetAllCarsFromTable
#Description: Gets the data of the cars in the database
def GetAllCarsFromTable():
    con = sqlite3.connect('car_Rental.db')

    carData = con.execute("SELECT * FROM cars")
    
    print("*** cars table ***")
    data = carData.fetchall()
    for row in data:
        print(row)

    print("\n*** maint_cars table ***")
    maintcarsData = con.execute("SELECT * FROM maint_cars")
    d = maintcarsData.fetchall()
    for i in d:
        print(i)

    con.commit()

    return carData
    
#Name: MoveCarToMaintenanceTable
#Description: Moves a car from the cars table to the maintenance table
def MoveCarToMaintenanceTable(car_vin):
    con = sqlite3.connect('car_Rental.db')

    #First check if the car exists in the cars table
    check = con.execute("SELECT vin FROM cars WHERE vin = ?", (car_vin,))

    if (check.fetchall() == []): return

    #Creates a new table if maint_cars doesn't exist
    con.execute("CREATE TABLE IF NOT EXISTS maint_cars (brand TEXT, model TEXT, year INTEGER, vin TEXT)")

    con.execute("INSERT INTO maint_cars SELECT * FROM cars WHERE vin = ?", (car_vin,))

    con.execute("DELETE FROM cars WHERE vin = ?", (car_vin,))

    con.commit()

#Name: MoveMaintCarToCarsTable
#Description: Moves a car from the maintenance table to the cars table
def MoveMaintCarToCarsTable(car_vin):
    con = sqlite3.connect('car_Rental.db')

    check = con.execute("SELECT vin FROM maint_cars WHERE vin = ?", (car_vin,))

    if (check.fetchall() == []): return

    con.execute("CREATE TABLE IF NOT EXISTS cars (brand TEXT, model TEXT, year INTEGER, vin TEXT)")

    con.execute("INSERT INTO cars SELECT * FROM maint_cars WHERE vin = ?", (car_vin,))

    con.execute("DELETE FROM maint_cars WHERE vin = ?", (car_vin,))

    con.commit()

#Name: AddColumnToCarsTable
#Description: Adds a vin column, data type TEXT to the cars table
#Note: Run this function if the database has not been updated with a new column for the vin
def AddColumnToCarsTable():
    con = sqlite3.connect('car_Rental.db')

    con.execute("ALTER TABLE cars ADD vin TEXT")

    con.commit()
