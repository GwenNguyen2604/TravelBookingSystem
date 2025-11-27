"""
    This module manages database
"""
import sqlite3
import os
import datetime
import database_logger


class CarsDatabase:
    """
    This class is the car database class
    """

    # Ensure the helper uses the same backend database file as the server.
    # This resolves relative-path issues when modules are imported from
    # different working directories.
    database = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'Database', 'cars.db')
    )

    def __init__(self):
        pass

    # *** MASTER TABLE ***

    @staticmethod
    @database_logger.DatabaseLogger.log_car_add_to_master_table
    def add_new_car_to_table(make, model, year, vin):
        """
        Description: Adds a car to the master table in the 'cars.db' database
        """
        con = sqlite3.connect(CarsDatabase.database)

        # Ensure master_table exists (with desired column order: vin first)
        con.execute("""
            CREATE TABLE IF NOT EXISTS master_table (
                vin TEXT,
                make TEXT,
                model TEXT,
                year INTEGER,
                class TEXT,
                electric TEXT,
                body TEXT
            )
        """)

        # Migration: add columns if table created earlier without them & reorder if needed
        cur = con.execute("PRAGMA table_info(master_table)")
        info_rows = cur.fetchall()
        existing_cols = [row[1] for row in info_rows]
        existing_set = set(existing_cols)
        for col, col_type in (
            ('class', 'TEXT'),
            ('electric', 'TEXT'),
            ('body', 'TEXT'),
        ):
            if col not in existing_set:
                try:
                    con.execute(f"ALTER TABLE master_table ADD COLUMN {col} {col_type}")
                except Exception:
                    pass
        # Reorder columns if vin is not first
        desired_order = ['vin','make','model','year','class','electric','body']
        if existing_cols and existing_cols != desired_order:
            try:
                con.execute("""
                    CREATE TABLE IF NOT EXISTS master_table_reordered (
                        vin TEXT,
                        make TEXT,
                        model TEXT,
                        year INTEGER,
                        class TEXT,
                        electric TEXT,
                        body TEXT
                    )
                """)
                con.execute("""
                    INSERT INTO master_table_reordered (vin, make, model, year, class, electric, body)
                    SELECT vin, make, model, year, class, electric, body FROM master_table
                """)
                con.execute("DROP TABLE master_table")
                con.execute("ALTER TABLE master_table_reordered RENAME TO master_table")
            except Exception:
                # if anything fails, keep existing table
                pass

        exists = con.execute(
            "SELECT 1 FROM master_table WHERE vin = ?",
            (vin,)
        ).fetchone()
        if exists:
            con.execute("""
                UPDATE master_table
                SET make=?, model=?, year=?
                WHERE vin=?
            """, (make, model, year, vin,))
        else:
            con.execute("""
                INSERT INTO master_table (vin, make, model, year, class, electric, body)
                VALUES (?, ?, ?, ?, NULL, NULL, NULL)
            """, (vin, make, model, year,))

        con.commit()
        con.close()

    @staticmethod
    def get_all_cars_from_master_table():
        """
        Description: Gets all car data from the master table in the
                     'cars.db' database
                     returns a sqlite object
        """
        con = sqlite3.connect(CarsDatabase.database)

        data = con.execute("SELECT * FROM master_table")

        con.commit()
        con.close()

        return data

    @staticmethod
    def check_if_database_exists():
        """
        Description: Returns true if the database exists,
                     otherwise returns false
        """
        return os.path.exists(CarsDatabase.database)

    # *** CAR ATTRIBUTE EXTENSIONS ***
    @staticmethod
    def update_car_specs(vin, car_class=None, electric=None, body=None):
        """Update extended car attributes for a VIN.

        Parameters may be left as None to skip updating that attribute.
        car_class: one of ('Luxury','Premium','Economy') or None
        electric: 'YES' / 'NO' / boolean or None
        body: one of ('Sedan','SUV','Truck') or None
        """
        con = sqlite3.connect(CarsDatabase.database)
        # ensure table has columns
        con.execute("""
            CREATE TABLE IF NOT EXISTS master_table (
                vin TEXT,
                make TEXT,
                model TEXT,
                year INTEGER,
                class TEXT,
                electric TEXT,
                body TEXT
            )
        """)
        # basic VIN existence check
        exists = con.execute("SELECT 1 FROM master_table WHERE vin = ?", (vin,)).fetchone()
        if not exists:
            con.close()
            return False

        fields = []
        values = []
        if car_class is not None:
            if car_class not in ('Luxury','Premium','Economy'):
                con.close()
                raise ValueError('Invalid car_class')
            fields.append('class = ?')
            values.append(car_class)
        if electric is not None:
            if isinstance(electric, bool):
                electric_val = 'YES' if electric else 'NO'
            else:
                electric_val = str(electric).upper()
            if electric_val not in ('YES','NO'):
                con.close()
                raise ValueError('Invalid electric value')
            fields.append('electric = ?')
            values.append(electric_val)
        if body is not None:
            if body not in ('Sedan','SUV','Truck'):
                con.close()
                raise ValueError('Invalid body value')
            fields.append('body = ?')
            values.append(body)

        if fields:
            values.append(vin)
            set_clause = ', '.join(fields)
            con.execute(f"UPDATE master_table SET {set_clause} WHERE vin = ?", tuple(values))
            con.commit()
        con.close()
        return True

    @staticmethod
    def get_car_specs(vin):
        """Return extended car attributes for a VIN as dict or None if not found."""
        con = sqlite3.connect(CarsDatabase.database)
        cur = con.execute("SELECT class, electric, body FROM master_table WHERE vin = ?", (vin,))
        row = cur.fetchone()
        con.close()
        if not row:
            return None
        return {'vin': vin, 'class': row[0], 'electric': row[1], 'body': row[2]}

    # *** RATING MANAGER ***

    @staticmethod
    def get_all_ratings(vin):
        """
        Description: returns a sqlite object containing all rating data
                     given a vin;
                     Returns nothing if there are no ratings
        """
        con = sqlite3.connect(CarsDatabase.database)

        database_logger.DatabaseLogger.log_rating_request(vin)

        exists = con.execute("""
                                SELECT *
                                FROM rating_master WHERE vin = ?
                             """, (vin,))

        if exists.arraysize == 0:
            database_logger.DatabaseLogger.log_failed_rating_request(vin)
            con.close()
            return None

        rating_data = con.execute("""
                                    SELECT *
                                    FROM ?_rating_comment_table
                                  """, (vin,))

        con.commit()
        con.close()

        return rating_data

    @staticmethod
    def add_new_rating_and_comment(vin, rating, comment):
        """
        Description: Adds a rating and a comment to a unique table for the vin;
                     Creates a new table if the vin doesn't exist
                     in the rating_master table
        """

        con = sqlite3.connect(CarsDatabase.database)
        date_time = datetime.datetime.now().isoformat()

        con.execute("""
                        CREATE TABLE IF NOT EXISTS ?_rating_comment_table (
                            rating TEXT,
                            comment TEXT,
                            datetime TEXT
                        )
                    """, (vin,))

        con.execute("""
                        INSERT INTO ?_rating_comment_table (
                            rating,
                            comment,
                            datetime
                        )
                        VALUES (?, ?, ?)
                    """, (vin, rating, comment, date_time,))

        database_logger.DatabaseLogger.log_rating_added_to_rating_table(
            vin, rating, comment, date_time
        )

        con.commit()
        con.close()
    # *** RENTAL PRICE MANAGER ***

    @staticmethod
    def add_rental_price_to_table(vin, price):
        """
        Description: Adds a rental price to a vin
                     if the vin doesn't exist in the table
        """
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("""
                        CREATE TABLE IF NOT EXISTS rental_price_table (
                            vin TEXT,
                            rental_price TEXT
                        )
                    """)

        exists = con.execute("""
                                SELECT 1
                                FROM rental_price_table
                                WHERE vin = ?
                             """, (vin,)).fetchone()

        if exists:
            database_logger.DatabaseLogger.log_rental_price_fail_added(vin)
            con.close()
            return

        con.execute("""
                        INSERT INTO rental_price_table (
                            vin,
                            rental_price
                        )
                        VALUES (?, ?)
                    """, (vin, price,))

        database_logger.DatabaseLogger.log_rental_price_added(vin, price)

        con.commit()
        con.close()

    @staticmethod
    def get_rental_price_from_table(vin):
        """
        Description: Gets a rental price from the table given a vin number;
                     Returns nothing if the vin doesn't exist
        """
        con = sqlite3.connect(CarsDatabase.database)

        exists = con.execute("""
                                SELECT 1
                                FROM rental_price_table
                                WHERE vin = ?
                             """, (vin,)).fetchone()

        if not exists:
            con.close()
            return None

        cur = con.execute("""
                                SELECT rental_price
                                FROM rental_price_table
                                WHERE vin = ?
                            """, (vin,))
        row = cur.fetchone()

        con.commit()
        con.close()

        return row[0] if row else None

    @staticmethod
    def get_all_rental_prices_from_table():
        """
        Description: Gets all rental prices and vins from the
                     rental_price_table as a sqlite object
        """
        con = sqlite3.connect(CarsDatabase.database)

        all_prices = con.execute("SELECT * FROM rental_price_table")

        con.commit()
        con.close()

        return all_prices

    @staticmethod
    def update_rental_price_in_table(vin, new_price):
        """
        Description: Sets a new price to an existing vin in the
                     rental_price_table. Returns if the vin doesn't exist
        """
        con = sqlite3.connect(CarsDatabase.database)

        exists = con.execute("""
                                SELECT *
                                FROM rental_price_table
                                WHERE vin = ?
                             """, (vin,))

        if exists.arraysize == 0:
            con.close()
            return

        con.execute("""
                        UPDATE rental_price_table
                        SET rental_price = ?
                        WHERE vin = ?
                    """, (new_price, vin,))

        con.commit()
        con.close()

    # *** STATUS MANAGER ***
    @staticmethod
    @database_logger.DatabaseLogger.log_new_status_add
    def add_new_status_to_table(vin, status):
        """
        Description: Adds a new vin to the table and sets the status;
        Returns if the vin already exists in the table
        """
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("""CREATE TABLE IF NOT EXISTS status_table (
                    vin TEXT,
                    status TEXT
        )""")

        # Check if the VIN already exists
        exists = con.execute(
            "SELECT 1 FROM status_table WHERE vin = ?",
            (vin,)
        ).fetchone()
        if exists:
            # Update the status for the existing VIN
            con.execute("""
                    UPDATE status_table SET status = ?
                    WHERE vin = ?
                """, (status, vin)
            )
        else:
            # Insert a new VIN and status
            con.execute("""
                    INSERT INTO status_table (vin, status)
                        VALUES (?, ?)
                """, (vin, status)
            )

        con.commit()
        con.close()

    @staticmethod
    @database_logger.DatabaseLogger.log_status_change
    def set_status_to_table(vin, status):
        """
        Description: Sets the status of a vin in the status table;
        Does nothing if the vin doesn't exist
        """
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("""CREATE TABLE IF NOT EXISTS status_table (
                    vin TEXT,
                    status TEXT
        )""")

        con.execute("""UPDATE status_table SET status = ? WHERE vin = ?
        """, (status, vin,))

        con.commit()
        con.close()

    @staticmethod
    @database_logger.DatabaseLogger.log_get_status_request
    def get_status_from_table(vin):
        """
        Description: Gets the status of a vin from the status table;
        Returns a sqlite object containing the status
        """
        con = sqlite3.connect(CarsDatabase.database)

        status = con.execute("SELECT status FROM status_table WHERE vin = ?"
        ,(vin,))

        con.commit()
        con.close()

        return status

    # *** RENTED CAR MANAGER ***
    @staticmethod
    def add_car_to_rented_table(vin, start_time, end_time):
        """
        Description: Adds a car to the rented table;
        The car will not added if it already exists in the table
        """
        con = sqlite3.connect(CarsDatabase.database)

        con.execute("""CREATE TABLE IF NOT EXISTS rented_table(
                    vin TEXT,
                    start_time TEXT,
                    end_time TEXT
        )""")

        con.execute("""INSERT INTO rented_table (vin, start_time, end_time)
        SELECT (?, ?, ?) WHERE NOT EXISTS (SELECT 1 FROM rented_table
        WHERE vin = ?)""", (vin, start_time, end_time, vin,))

        con.commit()
        con.close()

    @staticmethod
    def remove_car_from_rented_table(vin):
        """
        Description: Removes car from the rented_table table;
        Does not remove if the car doesn't exist in the table
        """
        con = sqlite3.connect(CarsDatabase.database)

        try:
            con.execute("""DELETE * FROM rented_table
                        WHERE vin = ?""", (vin,))
        except:
            print("WARNING: Attempted deletion from nonexistent rented_table")

        con.commit()
        con.close()

    # MAINTENANCE MANAGER
    @staticmethod
    def move_car_to_maintenance_table(vin):
        """
        // Function description
        """

    @staticmethod
    def set_time_in_maintenance(vin, time_in):
        """
        // Function description
        """

    @staticmethod
    def set_time_out_maintenance(vin, time_out):
        """
        // Function description
        """

    @staticmethod
    def set_service_performed_maintenance(vin, service_performed):
        """
        // Function description
        """

    @staticmethod
    def write_to_maintenance_log_table(
        vin,
        time_in,
        time_out,
        service_performed
    ):
        """
        // Function description
        """
