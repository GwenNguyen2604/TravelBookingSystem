import sqlite3

# Connect to the database
conn = sqlite3.connect("car_Rental.db")
cursor = conn.cursor()

# 1. Create the table with UNIQUE constraint to prevent future duplicates
#cursor.execute("""
#CREATE TABLE IF NOT EXISTS cars (
   # brand TEXT,
   # model TEXT,
  #  year INTEGER,
   # vin TEXT,  
 #   UNIQUE(brand, model, year, vin)
#)
#""")

# 2. Remove existing duplicates, keeping only the first occurrence
#cursor.execute("""
#DELETE FROM cars
#WHERE ROWID NOT IN (
#    SELECT MIN(ROWID)
#    FROM cars
#    GROUP BY brand, model, year, vin
#)
#""")

# 3. Insert new data — duplicates will be ignored
#cursor.execute("""
#INSERT OR IGNORE INTO cars (brand, model, year, vin) VALUES
#('', '', )
#""")

# 4. Commit changes
#conn.commit()

# 5. Fetch and print all rows
cursor.execute("SELECT * FROM cars")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 6. Close the connection
conn.close()


