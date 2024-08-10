from .database import pool

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