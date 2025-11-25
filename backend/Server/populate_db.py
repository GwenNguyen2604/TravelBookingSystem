#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Populate the database with sample vehicles and prices
This version works standalone without database_manager.py
"""
import sqlite3
import os

# Database path - adjusted for your folder structure
# From Server/ folder, go up to backend/, then to Database/cars.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, '..', 'Database', 'cars.db')
DB_FILE = os.path.abspath(DB_FILE)

# Sample vehicles data
vehicles = [
    {"make": "BMW", "model": "3 Series", "year": 2024, "vin": "BMW3SERIES2024001", "price": 89.00},
    {"make": "Mercedes", "model": "C-Class", "year": 2024, "vin": "MERCC CLASS2024001", "price": 95.00},
    {"make": "Tesla", "model": "Model 3", "year": 2023, "vin": "TESLAMODEL32023001", "price": 110.00},
    {"make": "Audi", "model": "A4", "year": 2024, "vin": "AUDIA4YR2024VIN001", "price": 92.00},
    {"make": "Lexus", "model": "ES", "year": 2023, "vin": "LEXUSES2023VIN0001", "price": 88.00},
    {"make": "Toyota", "model": "Camry", "year": 2024, "vin": "TOYOTACAMRY2024001", "price": 65.00},
    {"make": "Honda", "model": "Accord", "year": 2023, "vin": "HONDAACCORD2023001", "price": 62.00},
    {"make": "Kia", "model": "K5", "year": 2024, "vin": "KIAK5YEAR2024VN0001", "price": 58.00},
    {"make": "Hyundai", "model": "Sonata", "year": 2023, "vin": "HYUNDAISONATA23001", "price": 60.00},
]

def init_database():
    """Create the database and tables if they don't exist"""
    print("Database file path: {0}".format(DB_FILE))
    
    # Check if Database directory exists
    db_dir = os.path.dirname(DB_FILE)
    if not os.path.exists(db_dir):
        print("Creating Database directory: {0}".format(db_dir))
        os.makedirs(db_dir)
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS master_table (
            make TEXT,
            model TEXT,
            year INTEGER,
            vin TEXT PRIMARY KEY
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rental_price_table (
            vin TEXT PRIMARY KEY,
            rental_price REAL
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS status_table (
            vin TEXT PRIMARY KEY,
            status TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def populate_vehicles():
    """Add vehicles to the database"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    success_count = 0
    error_count = 0
    
    for vehicle in vehicles:
        try:
            # Insert or replace vehicle in master_table
            cur.execute("""
                INSERT OR REPLACE INTO master_table (make, model, year, vin)
                VALUES (?, ?, ?, ?)
            """, (vehicle["make"], vehicle["model"], vehicle["year"], vehicle["vin"]))
            
            # Insert or replace price
            cur.execute("""
                INSERT OR REPLACE INTO rental_price_table (vin, rental_price)
                VALUES (?, ?)
            """, (vehicle["vin"], vehicle["price"]))
            
            # Insert or replace status
            cur.execute("""
                INSERT OR REPLACE INTO status_table (vin, status)
                VALUES (?, ?)
            """, (vehicle["vin"], "AVAILABLE"))
            
            print("Added: {0} {1} ({2}) - ${3:.2f}/day - AVAILABLE".format(
                vehicle['make'], 
                vehicle['model'], 
                vehicle['year'],
                vehicle['price']
            ))
            
            success_count += 1
            
        except Exception as e:
            print("Error adding {0} {1}: {2}".format(
                vehicle['make'], 
                vehicle['model'], 
                str(e)
            ))
            error_count += 1
    
    conn.commit()
    conn.close()
    
    return success_count, error_count

def verify_data():
    """Verify that data was added correctly"""
    print("\nVerifying database contents...")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Count vehicles
    cur.execute("SELECT COUNT(*) FROM master_table")
    vehicle_count = cur.fetchone()[0]
    
    # Count prices
    cur.execute("SELECT COUNT(*) FROM rental_price_table")
    price_count = cur.fetchone()[0]
    
    conn.close()
    
    print("Total vehicles in database: {0}".format(vehicle_count))
    print("Total prices in database: {0}".format(price_count))

def main():
    print("=" * 60)
    print("POPULATING DATABASE WITH SAMPLE DATA")
    print("=" * 60)
    print("")
    
    # Initialize database
    init_database()
    
    print("\nAdding vehicles to database...")
    print("-" * 60)
    
    # Populate vehicles
    success_count, error_count = populate_vehicles()
    
    print("")
    print("-" * 60)
    
    # Verify data was added
    verify_data()
    
    print("")
    print("=" * 60)
    print("DATABASE POPULATION COMPLETE")
    print("=" * 60)
    print("Successfully added: {0} vehicles".format(success_count))
    if error_count > 0:
        print("Errors: {0}".format(error_count))
    
    print("\nNext steps:")
    print("1. Start the Flask server: python3 server.py")
    print("2. Open your frontend in a browser")
    print("3. The vehicles should load automatically!")
    print("")

if __name__ == "__main__":
    main()