import sqlite3
import os

#Name: CheckIfDatabaseExists
#Description: Returns true if the database exists, false otherwise
def CheckIfDatabaseExists():
    return os.path.exists('car_Rental.db')

#Name: WriteNewCarToTable
#Description: Creates a new car entry to the table in the database
def WriteNewCarToTable(brand_name, model_name, model_year):
    con = sqlite3.connect('car_Rental.db')
    cursor = con.cursor()

    cursor.execute("""
    INSERT INTO cars (brand, model, year) VALUES
    (brand_name, model_name, model_year)
    """)

    con.commit()

