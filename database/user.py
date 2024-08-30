from .database import pool
import os
import hashlib

def create_hash(text):
    combined = os.getenv("TOKEN_SECRET_KEY") + text
    hash_object = hashlib.sha256(combined.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex

def verify_password(username, password):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, username FROM user WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchall()[0]
        if user:
            return {"id": user[0], "username": user[1]}
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        db.close()

def get_username_by_id(id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT username FROM user WHERE id = %s", (id, ))
        user = cursor.fetchall()[0]
        if user:
            return user[0]
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        db.close()

def get_user_by_username(username):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM user WHERE username = %s", (username, ))
        user = cursor.fetchall()[0]
        if user:
            return user[0]
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        db.close()

def add_user(username, password):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

def add_google_user(id, username, user_email, user_photo):
    try:
        password = create_hash(username)
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user (id, username, password, email, photo) VALUES (%s, %s, %s, %s, %s)", (id, username, password, user_email, user_photo))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

def get_user_profile_by_id(id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT username, email, savings, photo FROM user WHERE id = %s
        """, (id, ))
        username, email, savings, photo = cursor.fetchall()[0]
        if username:
            return {
                "id": id,
                "username": username,
                "email": email,
                "savings": savings,
                "photo": photo
            }
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        db.close()

def get_savings(id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT savings FROM user WHERE id = %s", (id, ))
        savings = cursor.fetchall()[0][0]
        return savings
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

def update_buyer_savings(user_id, amount):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT savings FROM user WHERE id = %s", (user_id, ))
        savings = cursor.fetchall()[0][0]
        cursor.execute("UPDATE user SET savings = %s WHERE id = %s", (savings - amount, user_id))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()