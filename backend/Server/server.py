from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import datetime

BASE_DIR = os.path.dirname(__file__)
# point to backend/Database/cars.db after reorganization
DB_FILE = os.path.abspath(os.path.join(BASE_DIR, '..', 'Database', 'cars.db'))


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS master_table (
            make TEXT,
            model TEXT,
            year INTEGER,
            vin TEXT PRIMARY KEY
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS rental_price_table (
            vin TEXT PRIMARY KEY,
            rental_price REAL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS rented_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vin TEXT,
            start_time TEXT,
            end_time TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vin TEXT,
            rating INTEGER,
            comment TEXT,
            datetime TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def check_availability(vin, start_time, end_time):
    """
    Check if a vehicle is available for the given time period.
    Returns True if available, False if already booked.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Query for overlapping rentals
    # A rental overlaps if:
    # - New rental starts before existing ends AND new rental ends after existing starts
    cur.execute("""
        SELECT COUNT(*) as overlap_count
        FROM rented_table
        WHERE vin = ?
        AND (
            (start_time < ? AND end_time > ?)
            OR (start_time < ? AND end_time > ?)
            OR (start_time >= ? AND end_time <= ?)
        )
    """, (vin, end_time, start_time, end_time, start_time, start_time, end_time))
    
    result = cur.fetchone()
    conn.close()
    
    return result['overlap_count'] == 0


app = Flask(__name__)
CORS(app)


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """
    Get all vehicles. Optionally filter by availability for given dates.
    Query params: start_time, end_time (format: YYYY-MM-DD HH:MM)
    """
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT make, model, year, vin FROM master_table')
        rows = cur.fetchall()
        vehicles = [dict(row) for row in rows]
        
        # If dates provided, check availability for each vehicle
        if start_time and end_time:
            for vehicle in vehicles:
                vehicle['available'] = check_availability(
                    vehicle['vin'], 
                    start_time, 
                    end_time
                )
        else:
            # No dates provided, mark all as potentially available
            for vehicle in vehicles:
                vehicle['available'] = True
                
    except sqlite3.OperationalError:
        vehicles = []
    finally:
        conn.close()

    return jsonify({'vehicles': vehicles})


@app.route('/api/vehicles/<vin>', methods=['GET'])
def get_vehicle(vin):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT make, model, year, vin FROM master_table WHERE vin = ?', (vin,))
        row = cur.fetchone()
        if row is None:
            return jsonify({'error': 'vehicle not found'}), 404
        vehicle = dict(row)
        # attach price if available
        cur.execute('SELECT rental_price FROM rental_price_table WHERE vin = ?', (vin,))
        price_row = cur.fetchone()
        vehicle['rental_price'] = price_row['rental_price'] if price_row else None
    finally:
        conn.close()

    return jsonify(vehicle)


@app.route('/api/vehicles/<vin>/availability', methods=['GET'])
def check_vehicle_availability(vin):
    """
    Check if a specific vehicle is available for given dates.
    Query params: start_time, end_time (format: YYYY-MM-DD HH:MM)
    """
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not start_time or not end_time:
        return jsonify({'error': 'start_time and end_time are required'}), 400
    
    available = check_availability(vin, start_time, end_time)
    
    return jsonify({
        'vin': vin,
        'available': available,
        'start_time': start_time,
        'end_time': end_time
    })


@app.route('/api/prices', methods=['GET'])
def get_prices():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT vin, rental_price FROM rental_price_table')
        rows = cur.fetchall()
        prices = [dict(row) for row in rows]
    except sqlite3.OperationalError:
        prices = []
    finally:
        conn.close()

    return jsonify({'prices': prices})


@app.route('/api/bookings', methods=['POST'])
def create_booking():
    payload = request.get_json(force=True)
    vin = payload.get('vin')
    start_time = payload.get('start_time')
    end_time = payload.get('end_time')

    if not vin or not start_time or not end_time:
        return jsonify({'error': 'vin, start_time and end_time are required'}), 400

    # Check availability before booking
    if not check_availability(vin, start_time, end_time):
        return jsonify({
            'error': 'Vehicle is not available for the selected dates',
            'available': False
        }), 409  # 409 Conflict status code

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO rented_table (vin, start_time, end_time) VALUES (?, ?, ?)',
            (vin, start_time, end_time)
        )
        conn.commit()
        booking_id = cur.lastrowid
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

    conn.close()
    return jsonify({
        'status': 'booked',
        'booking_id': booking_id,
        'vin': vin,
        'start_time': start_time,
        'end_time': end_time
    }), 201


@app.route('/api/bookings/<vin>', methods=['GET'])
def get_vehicle_bookings(vin):
    """Get all bookings for a specific vehicle"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'SELECT id, vin, start_time, end_time FROM rented_table WHERE vin = ? ORDER BY start_time',
            (vin,)
        )
        rows = cur.fetchall()
        bookings = [dict(row) for row in rows]
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
    
    conn.close()
    return jsonify({'bookings': bookings})


@app.route('/api/ratings', methods=['POST'])
def add_rating():
    payload = request.get_json(force=True)
    vin = payload.get('vin')
    rating = payload.get('rating')
    comment = payload.get('comment', '')

    if not vin or rating is None:
        return jsonify({'error': 'vin and rating are required'}), 400

    dt = datetime.datetime.utcnow().isoformat()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO ratings (vin, rating, comment, datetime) VALUES (?, ?, ?, ?)',
            (vin, int(rating), comment, dt)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

    conn.close()
    return jsonify({'status': 'rating_added', 'vin': vin}), 201


if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)