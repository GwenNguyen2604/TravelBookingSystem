"""Interactive CLI for car database management.

Features:
1) Add new car (optional initial price, optional image copy by VIN naming)
2) Remove car by VIN (removes price, sets REMOVED status, deletes image)
3) Update car availability status (insert or update)
4) Update car rental price (insert or update)
5) List all cars (includes extended attributes)
6) Update extended attributes (class / electric / body)

Images are stored in `backend/Database/Images/` named `<VIN><ext>`.
Extended attributes stored in master_table columns: class, electric, body.
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

    image_path = input('Path to image file (optional, press enter to skip): ').strip()
    if image_path and os.path.exists(image_path) and os.path.isfile(image_path):
        images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database', 'Images'))
        os.makedirs(images_dir, exist_ok=True)
        _, ext = os.path.splitext(image_path)
        dest = os.path.join(images_dir, f"{vin}{ext}")
        try:
            shutil.copy(image_path, dest)
            print('Image copied to Images folder as', os.path.basename(dest))
        except Exception as e:
            print('Failed to copy image:', e)

    DB.add_new_car_to_table(make, model, year, vin)

    price_input = input('Initial rental price (per day, e.g. 49.99 or blank to skip): ').strip()
    if price_input:
        try:
            float(price_input)
        except Exception:
            print('Invalid price; skipped.')
        else:
            DB.add_rental_price_to_table(vin, price_input)
            print('Added initial price.')

    print('Car added.')


def remove_car_by_vin():
    vin = input('VIN to remove: ').strip()
    if not vin:
        print('No VIN provided.')
        return

    con = sqlite3.connect(DB.database)
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

    images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database', 'Images'))
    if os.path.isdir(images_dir):
        for name in os.listdir(images_dir):
            if name.startswith(vin):
                path = os.path.join(images_dir, name)
                try:
                    os.remove(path)
                    print('Removed image file:', name)
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
    print('Car removed.')


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
        print('VIN not found in master_table.')
        con.close()
        return
    con.close()

    DB.add_new_status_to_table(vin, status)
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
        print('VIN not found in master_table.')
        con.close()
        return
    con.close()

    existing = DB.get_rental_price_from_table(vin)
    if existing is None:
        DB.add_rental_price_to_table(vin, new_price)
        print('Price created.')
    else:
        DB.update_rental_price_in_table(vin, new_price)
        print('Price updated.')


def update_attributes_by_vin():
    vin = input('VIN to update attributes for: ').strip()
    if not vin:
        print('No VIN provided.')
        return
    con = sqlite3.connect(DB.database)
    cur = con.cursor()
    cur.execute('SELECT 1 FROM master_table WHERE vin = ?', (vin,))
    if not cur.fetchone():
        print('VIN not found in master_table.')
        con.close()
        return
    con.close()

    car_class = input('Class (Luxury/Premium/Economy or blank): ').strip()
    car_class = car_class if car_class in ('Luxury','Premium','Economy') else None
    electric = input('Electric (YES/NO or blank): ').strip().upper()
    electric = electric if electric in ('YES','NO') else None
    body = input('Body (Sedan/SUV/Truck or blank): ').strip()
    body = body if body in ('Sedan','SUV','Truck') else None

    if not any([car_class, electric, body]):
        print('No valid attributes provided.')
        return
    try:
        DB.update_car_specs(vin, car_class=car_class, electric=electric, body=body)
        print('Attributes updated.')
    except Exception as e:
        print('Failed to update attributes:', e)


def list_all_cars():
    con = sqlite3.connect(DB.database)
    cur = con.execute('SELECT make, model, year, vin, class, electric, body FROM master_table')
    rows = cur.fetchall()
    if not rows:
        print('No cars found.')
        con.close()
        return
    for make, model, year, vin, car_class, electric, body in rows:
        price = None
        status = None
        try:
            prow = con.execute('SELECT rental_price FROM rental_price_table WHERE vin = ?', (vin,)).fetchone()
            price = prow[0] if prow else None
        except Exception:
            pass
        try:
            srow = con.execute('SELECT status FROM status_table WHERE vin = ?', (vin,)).fetchone()
            status = srow[0] if srow else None
        except Exception:
            pass
        print(f"{make} {model} ({year}) VIN:{vin} | Price:{price if price is not None else 'N/A'} | Status:{status if status else 'N/A'} | Class:{car_class or '-'} | Electric:{electric or '-'} | Body:{body or '-'}")
    con.close()


def main():
    MENU = '''\
Choose an option:
1) Add new car (and optional initial price)
2) Update extended attributes (class/electric/body)
3) Remove car by VIN
4) Update car availability status
5) Update car price
6) List all cars
q) Quit
'''
    while True:
        print(MENU)
        choice = input('> ').strip().lower()
        if choice == '1':
            add_new_car_interactive()
        elif choice == '2':
            update_attributes_by_vin()
        elif choice == '3':
            remove_car_by_vin()
        elif choice == '4':
            update_status_by_vin()
        elif choice == '5':
            update_price_by_vin()
        elif choice == '6':
            list_all_cars()
        elif choice in ('q','quit','exit'):
            print('Goodbye')
            break
        else:
            print('Unknown option')


if __name__ == '__main__':
    main()
