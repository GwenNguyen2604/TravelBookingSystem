import sqlite3

# Connect to the database
conn = sqlite3.connect("car_Rental.db")
cursor = conn.cursor()

# 1. Create the table (if it doesn't exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    brand TEXT,
    model TEXT,
    year INTEGER
)
""")

# 2. Insert data (make sure strings are quoted properly)
cursor.execute("""
INSERT INTO cars (brand, model, year) VALUES
('Ferrari', 'CLassi12', 2025),
('Tesla', 'Model S', 2018)
""")

# 3. Commit changes
conn.commit()

# 4. Select all data from the cars table
res = cursor.execute("SELECT * FROM cars")

# 5. Fetch and print results
rows = res.fetchall()
for row in rows:
    print(row)

# 6. Close the connection
conn.close()
