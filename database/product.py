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
            SELECT product.name, price, rating_avg, review_count, description, specification, image_urls, user.username, file_size
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
                "images": None,
                "file_size": data[8]
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

def add_product(product_name, user_id, price, image_urls, thumbnail_url, description, specification, file_type, file_size, stock, source_url):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO product
            (name, owner_id, price, image_urls, thumbnail_url, description, specification, file_type, file_size, stock, source_url) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (product_name, user_id, price, image_urls, thumbnail_url, description, specification, file_type, file_size, stock, source_url))
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()
