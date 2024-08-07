from .database import pool
import json

def get_published_products():
    try:
        result = []
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.id, product.name, user.username, price, rating_avg, review_count, thumbnail_url
            FROM product INNER JOIN user 
            ON product.owner_id = user.id
            WHERE status = 1;""")
        data = cursor.fetchall()
        print(data)
        for item in data:
            result.append({
                "id": item[0],
                "name": item[1],
                "owner_name": item[2],
                "rating_avg": item[4],
                "review_count": item[5],
                "price": item[3],
                "thumbnail_url": item[6]
            })
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def get_product(id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.name, price, rating_avg, review_count, description, specification, image_urls, user.username
            FROM product INNER JOIN user 
            ON product.owner_id = user.id
            WHERE status = 1 AND product.id = %s;""", (id, ))
        data = cursor.fetchall()[0]
        result = {
            "user": {
                "username": data[7]
            },
            "product": {
                "name": data[0],
                "price": data[1],
                "rating_avg": data[2],
                "review_count": data[3],
                "description": data[4],
                "specification": None,
                "images": None
            }
        }
        if data[5]:
            temp_spec = []
            specs = data[5].split(",, ")
            for spec in specs:
                spec = json.loads(spec)
                temp_spec.append(spec)
            result["product"]["specification"] = temp_spec
        if data[6]:
            temp_img = []
            imgs = data[6].split(", ")
            for img in imgs:
                temp_img.append(img)
            result["product"]["images"] = temp_img
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def add_product(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute()
        
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def verify_password(username, password) -> dict:
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
    finally:
        cursor.close()
        db.close()