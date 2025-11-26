import datetime
from user_database import get_db
from user_security import hash_password, verify_password

def add_user(username, password, email):
    conn = get_db()
    cur = conn.cursor()

    try:
        hashed = hash_password(password)
        cur.execute("""
            INSERT INTO users (username, password, email)
            VALUES (?, ?, ?)
        """, (username, hashed, email))

        conn.commit()
        print("User created successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()


def check_login(username, password):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT password, is_active FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    if row is None:
        conn.close()
        return False

    stored_password, is_active = row

    if not is_active:
        conn.close()
        return False

    if verify_password(stored_password, password):
        # update last login time
        cur.execute("""
            UPDATE users SET last_login = ?
            WHERE username = ?
        """, (datetime.datetime.now(), username))
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


def delete_user(username):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()

    deleted = cur.rowcount > 0
    conn.close()

    return deleted


def deactivate_user(username):
    """Soft delete instead of removing."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE users SET is_active = 0 WHERE username = ?", (username,))
    conn.commit()
    result = cur.rowcount > 0
    conn.close()
    return result