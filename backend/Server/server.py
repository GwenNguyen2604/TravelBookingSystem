from flask import Flask, jsonify, request
from flask import send_from_directory, abort
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


app = Flask(__name__)
CORS(app)


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
            cur.execute('SELECT make, model, year, vin FROM master_table')
            rows = cur.fetchall()
            vehicles = [dict(row) for row in rows]
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



@app.route('/api/vehicles/<vin>/image', methods=['GET'])
def get_vehicle_image(vin):
    """Serve the image file named by VIN from `Database/Images`.

    Tries common extensions; 404 if none found.
    """
    images_dir = os.path.abspath(os.path.join(BASE_DIR, '..', 'Database', 'Images'))
    if not os.path.isdir(images_dir):
        abort(404)

    # Try common extensions
    exts = ['.jpg', '.jpeg', '.png', '.webp', '.avif']
    for ext in exts:
        candidate = f"{vin}{ext}"
        candidate_path = os.path.join(images_dir, candidate)
        if os.path.exists(candidate_path):
            return send_from_directory(images_dir, candidate)

    # Fallback: scan dir for any matching prefix
    try:
        for name in os.listdir(images_dir):
            if name.startswith(vin + '.') or name.startswith(vin):
                return send_from_directory(images_dir, name)
    except Exception:
        pass

    abort(404)


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

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO rented_table (vin, start_time, end_time) VALUES (?, ?, ?)',
            (vin, start_time, end_time)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

    conn.close()
    return jsonify({'status': 'booked', 'vin': vin}), 201


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
