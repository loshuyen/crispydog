from .database import pool
import json

def get_published_products(keyword):
    try:
        result = []
        db = pool.get_connection()
        cursor = db.cursor()
        if not keyword:
            cursor.execute("""
                SELECT product.id, product.name, user.username, price, rating_avg, review_count, thumbnail_url
                FROM product INNER JOIN user 
                ON product.owner_id = user.id
                WHERE status = 1 
                ORDER BY product.created_at DESC;""")
        else:
            cursor.execute("""
                SELECT product.id, product.name, user.username, price, rating_avg, review_count, thumbnail_url
                FROM product INNER JOIN user 
                ON product.owner_id = user.id
                WHERE status = 1 AND product.name LIKE %s 
                ORDER BY product.created_at DESC;""", (f"%{keyword}%", ))
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
        return None
    finally:
        cursor.close()
        db.close()

def get_product(id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.name, price, rating_avg, review_count, introduction, specification, image_urls, user.username, file_size, user.id, product.id
            FROM product INNER JOIN user 
            ON product.owner_id = user.id
            WHERE status = 1 AND product.id = %s;""", (id, ))
        data = cursor.fetchall()[0]
        result = {
            "product": {
                "id": data[10],
                "name": data[0],
                "price": data[1],
                "rating_avg": data[2],
                "review_count": data[3],
                "introduction": data[4],
                "specification": None,
                "images": data[6],
                "file_size": data[8],
                "user": {
                    "id": data[9],
                    "username": data[7]
                }
            }
        }
        if data[5]:
            result["product"]["specification"] = json.loads(data[5])
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def add_product(product_name, user_id, price, image_urls, thumbnail_url, introduction, specification, file_type, file_size, stock, source_url):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO product
            (name, owner_id, price, image_urls, thumbnail_url, introduction, specification, file_type, file_size, stock, source_url) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (product_name, user_id, price, image_urls, thumbnail_url, introduction, json.dumps(specification), file_type, file_size, stock, source_url))
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def toggle_my_product(user_id, product_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT status FROM product WHERE owner_id = %s AND id = %s;", (user_id, product_id))
        data = cursor.fetchall()
        if not data:
            raise 
        status = 0 if data[0][0] == 1 else 1
        cursor.execute("UPDATE product SET status = %s WHERE owner_id = %s AND id = %s;", (status, user_id, product_id))
        db.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()