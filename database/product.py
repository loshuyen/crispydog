from .database import pool
import json

def get_published_products(keyword, product_type):
    try:
        result = []
        db = pool.get_connection()
        cursor = db.cursor()
        params = None
        base_statement = "SELECT product.id, product.name, user.username, price, rating_avg, review_count, thumbnail_url, product_type FROM product INNER JOIN user ON product.owner_id = user.id WHERE status = 1"
        statement = None
        if keyword and product_type:
            statement = f"{base_statement} AND product.name LIKE %s AND product_type = %s ORDER BY product.created_at DESC"
            params = (f"%{keyword}%", product_type)
        elif not keyword and product_type:
            statement = f"{base_statement} AND product_type = %s ORDER BY product.created_at DESC"
            params = (product_type, )
        elif keyword and not product_type:
            statement = f"{base_statement} AND product.name LIKE %s ORDER BY product.created_at DESC"
            params = (f"%{keyword}%", )
        else:
            statement = base_statement
            params = None
        cursor.execute(statement, params)
        data = cursor.fetchall()
        for item in data:
            result.append({
                "id": item[0],
                "name": item[1],
                "owner_name": item[2],
                "rating_avg": item[4],
                "review_count": item[5],
                "price": item[3],
                "thumbnail_url": item[6],
                "product_type": item[7]
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
            SELECT product.name, price, rating_avg, review_count, introduction, specification, image_urls, user.username, file_size, user.id, product.id, product_type
            FROM product INNER JOIN user 
            ON product.owner_id = user.id
            WHERE status = 1 AND product.id = %s;""", (id, ))
        data = cursor.fetchall()[0]
        result = {
            "product": {
                "id": data[10],
                "name": data[0],
                "price": data[1],
                "product_type": data[11],
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

def add_product(product_name, user_id, price, image_urls, thumbnail_url, introduction, specification, file_type, file_size, stock, source_url, product_type):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO product
            (name, owner_id, price, image_urls, thumbnail_url, introduction, specification, file_type, file_size, stock, source_url, product_type) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (product_name, user_id, price, image_urls, thumbnail_url, introduction, json.dumps(specification), file_type, file_size, stock, source_url, product_type))
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

def get_owner_by_product_id(id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT owner_id
            FROM product INNER JOIN user ON product.owner_id = user.id
            WHERE product.id = %s;""", (id, ))
        owner_id = cursor.fetchall()[0][0]
        return owner_id
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()