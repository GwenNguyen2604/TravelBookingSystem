"""Interactive CLI for changing the car database.

Prompts for an optional image path when adding a car; copies image into
`backend/Database/Images/` using the VIN as filename. When removing a car,
the image file (if present) is removed from disk and the DB entry is removed.
"""

import os
import sqlite3
import uuid
import shutil

import database_manager

DB = database_manager.CarsDatabase


def generate_vin():
    return uuid.uuid4().hex[:17].upper()


def add_new_car_interactive():
    make = input('Make: ').strip()
    model = input('Model: ').strip()
    year_str = input('Year: ').strip()
    try:
        year = int(year_str)
    except Exception:
        print('Invalid year; aborting.')
        return

    vin = generate_vin()
    print(f'Generated VIN: {vin}')

    # Ask for optional image path; if provided and exists, copy into Images folder
    image_path = input('Path to image file (optional, press enter to skip): ').strip()
    image_filename = None
    if image_path:
        if os.path.exists(image_path) and os.path.isfile(image_path):
            images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database', 'Images'))
            os.makedirs(images_dir, exist_ok=True)
            _, ext = os.path.splitext(image_path)
            image_filename = f"{vin}{ext}"
            dest = os.path.join(images_dir, image_filename)
            try:
                shutil.copy(image_path, dest)
                print('Image copied to Images folder as', image_filename)
            except Exception as e:
                print('Failed to copy image:', e)
                image_filename = None
        else:
            print('Image path not found or not a file; skipping image.')

    # Create car entry
    DB.add_new_car_to_table(make, model, year, vin)

    price = input('Initial rental price (per day, e.g. 49.99): ').strip()
    try:
        float(price)
    except Exception:
        print('Invalid price; skipping price insert.')
        return

    DB.add_rental_price_to_table(vin, price)
    print('Added car and initial price.')


def remove_car_by_vin():
    vin = input('VIN to remove: ').strip()
    if not vin:
        print('No VIN provided.')
        return

    db_path = DB.database
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
    if not cur.fetchone():
        print('VIN not found in master_table.')
        con.close()
        return

    # Attempt to remove price row
    try:
        cur.execute('DELETE FROM rental_price_table WHERE vin = ?', (vin,))
    except Exception:
        pass

    # Attempt to remove associated image file by VIN naming (if any)
    try:
        images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database', 'Images'))
        exts = ['.jpg', '.jpeg', '.png', '.webp', '.avif']
        removed = False
        for ext in exts:
            candidate = os.path.join(images_dir, f"{vin}{ext}")
            if os.path.exists(candidate):
                os.remove(candidate)
                print('Removed image file:', os.path.basename(candidate))
                removed = True
                break
        if not removed:
            # fallback: scan for any filename beginning with VIN
            for name in os.listdir(images_dir):
                if name.startswith(vin):
                    p = os.path.join(images_dir, name)
                    try:
                        os.remove(p)
                        print('Removed image file:', name)
                        break
                    except Exception:
                        pass
    except Exception:
        pass

    # Set status to REMOVED (insert or update)
    try:
        cur.execute('CREATE TABLE IF NOT EXISTS status_table (vin TEXT, status TEXT)')
        cur.execute('SELECT 1 FROM status_table WHERE vin = ?', (vin,))
        if cur.fetchone():
            cur.execute('UPDATE status_table SET status = ? WHERE vin = ?', ('REMOVED', vin))
        else:
            cur.execute('INSERT INTO status_table (vin, status) VALUES (?, ?)', (vin, 'REMOVED'))
    except Exception as e:
        print('Warning: failed to set REMOVED status:', e)

    # Remove from master table
    try:
        cur.execute('DELETE FROM master_table WHERE vin = ?', (vin,))
    except Exception as e:
        print('Failed to delete from master_table:', e)
        con.rollback()
        con.close()
        return

    con.commit()
    con.close()
    print('Removed VIN from master_table, deleted price row, set status to REMOVED.')


def update_status_by_vin():
    vin = input('VIN to update status for: ').strip()
    if not vin:
        print('No VIN provided.')
        return
    status = input('New status (e.g. AVAILABLE, RENTED, MAINTENANCE): ').strip()
    if not status:
        print('No status provided.')
        return

    con = sqlite3.connect(DB.database)
    cur = con.cursor()
    cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
    if not cur.fetchone():
        print('VIN not found in master_table. Cannot update status for non-existing car.')
        con.close()
        return
    con.close()

    # Upsert status: add_new_status_to_table will insert or update as needed
    DB.add_new_status_to_table(vin, status)
    print('Status set.')


def update_price_by_vin():
    vin = input('VIN to update price for: ').strip()
    if not vin:
        print('No VIN provided.')
        return
    new_price = input('New price (e.g. 79.99): ').strip()
    try:
        float(new_price)
    except Exception:
        print('Invalid price; aborting.')
        return

    con = sqlite3.connect(DB.database)
    cur = con.cursor()
    cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
    if not cur.fetchone():
        print('VIN not found in master_table. Cannot update price for non-existing car.')
        con.close()
        return
    con.close()

    existing = DB.get_rental_price_from_table(vin)
    if existing is None:
        DB.add_rental_price_to_table(vin, new_price)
        print('Price row created.')
    else:
        DB.update_rental_price_in_table(vin, new_price)
        print('Price updated.')


def list_all_cars():
    con = sqlite3.connect(DB.database)
    cur = con.execute('SELECT make, model, year, vin FROM master_table')
    rows = cur.fetchall()
    if not rows:
        print('No cars found.')
        con.close()
        return

    for make, model, year, vin in rows:
        price = None
        status = None
        try:
            pcur = con.execute('SELECT rental_price FROM rental_price_table WHERE vin = ?', (vin,))
            prow = pcur.fetchone()
            price = prow[0] if prow else None
        except Exception:
            price = None

        try:
            scur = con.execute('SELECT status FROM status_table WHERE vin = ?', (vin,))
            srow = scur.fetchone()
            status = srow[0] if srow else None
        except Exception:
            status = None

        print(f"{make} {model} ({year}) VIN: {vin} | Price: {price if price is not None else 'N/A'} | Status: {status if status is not None else 'N/A'}")

    con.close()


def main():
    MENU = '''\
Choose an option:
1) Add new car (and initial price)
2) Remove car by VIN
3) Update car availability status
4) Update car price
5) List all cars
q) Quit
'''

    while True:
        print(MENU)
        choice = input('> ').strip().lower()
        if choice == '1':
            add_new_car_interactive()
        elif choice == '2':
            remove_car_by_vin()
        elif choice == '3':
            update_status_by_vin()
        elif choice == '4':
            update_price_by_vin()
        elif choice == '5':
            list_all_cars()
        elif choice in ('q', 'quit', 'exit'):
            print('Goodbye')
            break
        else:
            print('Unknown option')


if __name__ == '__main__':
    main()
"""
Interactive CLI for changing the car database.

This is a copy of the `car_database_main.py` interactive tool under your
requested filename so you can run `interactive_car_database_change.py` directly.
"""

import os
import sqlite3
import uuid
from datetime import datetime

import database_manager
import shutil

DB = database_manager.CarsDatabase


def generate_vin():
    return uuid.uuid4().hex[:17].upper()


def add_new_car_interactive():
    make = input('Make: ').strip()
    model = input('Model: ').strip()
    year_str = input('Year: ').strip()
    try:
        year = int(year_str)
    except Exception:
        print('Invalid year; aborting.')
        return

    vin = generate_vin()
    print(f'Generated VIN: {vin}')
	# Ask for optional image path; if provided and exists, copy into Images folder
    image_path = input('Path to image file (optional, press enter to skip): ').strip()
    image_filename = None
    if image_path:
        if os.path.exists(image_path) and os.path.isfile(image_path):
            images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database', 'Images'))
            os.makedirs(images_dir, exist_ok=True)
			# preserve extension, name by vin
            _, ext = os.path.splitext(image_path)
            image_filename = f"{vin}{ext}"
            dest = os.path.join(images_dir, image_filename)
            try:
                shutil.copy(image_path, dest)
                print('Image copied to Images folder as', image_filename)
            except Exception as e:
                print('Failed to copy image:', e)
                image_filename = None
        else:
            print('Image path not found or not a file; skipping image.')

    DB.add_new_car_to_table(make, model, year, vin)
    # set image_link in master_table if we copied a file
    if image_filename:
        # update master_table image_link directly
        con = sqlite3.connect(DB.database)
        con.execute('UPDATE master_table SET image_link = ? WHERE vin = ?', (image_filename, vin))
        con.commit()
        con.close()

    price = input('Initial rental price (per day, e.g. 49.99): ').strip()
    try:
        float(price)
    except Exception:
        print('Invalid price; skipping price insert.')
        return

    DB.add_rental_price_to_table(vin, price)
    print('Added car and initial price.')


def remove_car_by_vin():
    vin = input('VIN to remove: ').strip()
    if not vin:
        print('No VIN provided.')
        return

    db_path = DB.database
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
    if not cur.fetchone():
        print('VIN not found in master_table.')
        con.close()
        return

    try:
        cur.execute('DELETE FROM rental_price_table WHERE vin = ?', (vin,))
    except Exception:
        pass
    # Attempt to remove associated image file from Images folder (if any)
    try:
        images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database', 'Images'))
        # read image_link
        cur.execute('SELECT image_link FROM master_table WHERE vin = ?', (vin,))
        row = cur.fetchone()
        if row:
            image_name = row[0]
            if image_name:
                image_path_on_disk = os.path.join(images_dir, image_name)
                try:
                    if os.path.exists(image_path_on_disk):
                        os.remove(image_path_on_disk)
                        print('Removed image file:', image_name)
                except Exception:
                    pass
    except Exception:
        pass
    try:
        cur.execute('CREATE TABLE IF NOT EXISTS status_table (vin TEXT, status TEXT)')
        cur.execute('SELECT 1 FROM status_table WHERE vin = ?', (vin,))
        if cur.fetchone():
            cur.execute('UPDATE status_table SET status = ? WHERE vin = ?', ('REMOVED', vin))
        else:
            cur.execute('INSERT INTO status_table (vin, status) VALUES (?, ?)', (vin, 'REMOVED'))
    except Exception as e:
        print('Warning: failed to set REMOVED status:', e)

    try:
        cur.execute('DELETE FROM master_table WHERE vin = ?', (vin,))
    except Exception as e:
        print('Failed to delete from master_table:', e)
        con.rollback()
        con.close()
        return

    con.commit()
    con.close()
    print('Removed VIN from master_table, deleted price row, set status to REMOVED.')


def update_status_by_vin():
    vin = input('VIN to update status for: ').strip()
    if not vin:
        print('No VIN provided.')
        return
    status = input('New status (e.g. AVAILABLE, RENTED, MAINTENANCE): ').strip()
    if not status:
        print('No status provided.')
        return

    con = sqlite3.connect(DB.database)
    cur = con.cursor()
    cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
    if not cur.fetchone():
        print('VIN not found in master_table. Cannot update status for non-existing car.')
        con.close()
        return
    con.close()

    DB.set_status_to_table(vin, status)
    print('Status updated.')


def update_price_by_vin():
    vin = input('VIN to update price for: ').strip()
    if not vin:
        print('No VIN provided.')
        return
    new_price = input('New price (e.g. 79.99): ').strip()
    try:
        float(new_price)
    except Exception:
        print('Invalid price; aborting.')
        return

    con = sqlite3.connect(DB.database)
    cur = con.cursor()
    cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
    if not cur.fetchone():
        print('VIN not found in master_table. Cannot update price for non-existing car.')
        con.close()
        return
    con.close()

    existing = DB.get_rental_price_from_table(vin)
    if existing is None:
        DB.add_rental_price_to_table(vin, new_price)
        print('Price row created.')
    else:
        DB.update_rental_price_in_table(vin, new_price)
        print('Price updated.')


def list_all_cars():
    con = sqlite3.connect(DB.database)
    cur = con.execute('SELECT make, model, year, vin FROM master_table')
    rows = cur.fetchall()
    if not rows:
        print('No cars found.')
        con.close()
        return

    for make, model, year, vin in rows:
        price = None
        status = None
        try:
            pcur = con.execute('SELECT rental_price FROM rental_price_table WHERE vin = ?', (vin,))
            prow = pcur.fetchone()
            price = prow[0] if prow else None
        except Exception:
            price = None

        try:
            scur = con.execute('SELECT status FROM status_table WHERE vin = ?', (vin,))
            srow = scur.fetchone()
            status = srow[0] if srow else None
        except Exception:
            status = None

        print(f"{make} {model} ({year}) VIN: {vin} | Price: {price if price is not None else 'N/A'} | Status: {status if status is not None else 'N/A'}")

    con.close()


def main():
    MENU = '''\
Choose an option:
1) Add new car (and initial price)
2) Remove car by VIN
3) Update car availability status
4) Update car price
5) List all cars
q) Quit
'''

    while True:
        print(MENU)
        choice = input('> ').strip().lower()
        if choice == '1':
            add_new_car_interactive()
        elif choice == '2':
            remove_car_by_vin()
        elif choice == '3':
            update_status_by_vin()
        elif choice == '4':
            update_price_by_vin()
        elif choice == '5':
            list_all_cars()
        elif choice in ('q', 'quit', 'exit'):
            print('Goodbye')
            break
        else:
            print('Unknown option')


if __name__ == '__main__':
    main()
"""
Command-line helper to manage the cars database.

Options implemented:
 1) Add new car (generates a unique VIN, inserts into master_table,
	and prompts to add an initial rental price)
 2) Remove a car based on VIN (removes from master_table and related
	tables: rental_price_table, status_table)
 3) Update a car's availability status (uses VIN to look up)
 4) Update a car's price (uses VIN to look up)

This script uses the helper functions in `database_manager.CarsDatabase` where
available and runs SQL directly for removal operations.
"""

import os
import sqlite3
import uuid
from datetime import datetime

import database_manager

DB = database_manager.CarsDatabase


def generate_vin():
	# simple VIN-like unique id (17 chars) using uuid4
	return uuid.uuid4().hex[:17].upper()


def add_new_car_interactive():
	make = input('Make: ').strip()
	model = input('Model: ').strip()
	year_str = input('Year: ').strip()
	try:
		year = int(year_str)
	except Exception:
		print('Invalid year; aborting.')
		return

	vin = generate_vin()
	print(f'Generated VIN: {vin}')

	DB.add_new_car_to_table(make, model, year, vin)

	price = input('Initial rental price (per day, e.g. 49.99): ').strip()
	try:
		# store as numeric value (string accepted by DB helper)
		float(price)
	except Exception:
		print('Invalid price; skipping price insert.')
		return

	DB.add_rental_price_to_table(vin, price)
	print('Added car and initial price.')


def remove_car_by_vin():
	vin = input('VIN to remove: ').strip()
	if not vin:
		print('No VIN provided.')
		return

	db_path = DB.database
	con = sqlite3.connect(db_path)
	cur = con.cursor()

	# Check exists
	cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
	if not cur.fetchone():
		print('VIN not found in master_table.')
		con.close()
		return
	# Delete price row if present
	try:
		cur.execute('DELETE FROM rental_price_table WHERE vin = ?', (vin,))
	except Exception:
		pass

	# Set status to REMOVED (insert or update)
	try:
		cur.execute('CREATE TABLE IF NOT EXISTS status_table (vin TEXT, status TEXT)')
		cur.execute('SELECT 1 FROM status_table WHERE vin = ?', (vin,))
		if cur.fetchone():
			cur.execute('UPDATE status_table SET status = ? WHERE vin = ?', ('REMOVED', vin))
		else:
			cur.execute('INSERT INTO status_table (vin, status) VALUES (?, ?)', (vin, 'REMOVED'))
	except Exception as e:
		print('Warning: failed to set REMOVED status:', e)

	# Remove from master table
	try:
		cur.execute('DELETE FROM master_table WHERE vin = ?', (vin,))
	except Exception as e:
		print('Failed to delete from master_table:', e)
		con.rollback()
		con.close()
		return

	con.commit()
	con.close()
	print('Removed VIN from master_table, deleted price row, set status to REMOVED.')


def update_status_by_vin():
	vin = input('VIN to update status for: ').strip()
	if not vin:
		print('No VIN provided.')
		return
	status = input('New status (e.g. AVAILABLE, RENTED, MAINTENANCE): ').strip()
	if not status:
		print('No status provided.')
		return
	# Verify the VIN exists in master_table before changing status
	con = sqlite3.connect(DB.database)
	cur = con.cursor()
	cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
	if not cur.fetchone():
		print('VIN not found in master_table. Cannot update status for non-existing car.')
		con.close()
		return
	con.close()

	# use set_status_to_table which will update existing vin; if not present,
	# create a new status row
	DB.set_status_to_table(vin, status)
	print('Status updated.')


def update_price_by_vin():
	vin = input('VIN to update price for: ').strip()
	if not vin:
		print('No VIN provided.')
		return
	new_price = input('New price (e.g. 79.99): ').strip()
	try:
		float(new_price)
	except Exception:
		print('Invalid price; aborting.')
		return
	# Verify VIN exists in master_table before changing price
	con = sqlite3.connect(DB.database)
	cur = con.cursor()
	cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
	if not cur.fetchone():
		print('VIN not found in master_table. Cannot update price for non-existing car.')
		con.close()
		return
	con.close()

	# if price exists, update, otherwise add
	existing = DB.get_rental_price_from_table(vin)
	if existing is None:
		DB.add_rental_price_to_table(vin, new_price)
		print('Price row created.')
	else:
		DB.update_rental_price_in_table(vin, new_price)
		print('Price updated.')


def list_all_cars():
	con = sqlite3.connect(DB.database)
	cur = con.execute('SELECT make, model, year, vin FROM master_table')
	rows = cur.fetchall()
	if not rows:
		print('No cars found.')
		con.close()
		return

	for make, model, year, vin in rows:
		# fetch price and status (tables may not exist)
		price = None
		status = None
		try:
			pcur = con.execute('SELECT rental_price FROM rental_price_table WHERE vin = ?', (vin,))
			prow = pcur.fetchone()
			price = prow[0] if prow else None
		except Exception:
			price = None

		try:
			scur = con.execute('SELECT status FROM status_table WHERE vin = ?', (vin,))
			srow = scur.fetchone()
			status = srow[0] if srow else None
		except Exception:
			status = None

		print(f"{make} {model} ({year}) VIN: {vin} | Price: {price if price is not None else 'N/A'} | Status: {status if status is not None else 'N/A'}")

	con.close()


def main():
	MENU = '''\
Choose an option:
1) Add new car (and initial price)
2) Remove car by VIN
3) Update car availability status
4) Update car price
5) List all cars
q) Quit
'''

	while True:
		print(MENU)
		choice = input('> ').strip().lower()
		if choice == '1':
			add_new_car_interactive()
		elif choice == '2':
			remove_car_by_vin()
		elif choice == '3':
			update_status_by_vin()
		elif choice == '4':
			update_price_by_vin()
		elif choice == '5':
			list_all_cars()
		elif choice in ('q', 'quit', 'exit'):
			print('Goodbye')
			break
		else:
			print('Unknown option')


if __name__ == '__main__':
	main()
