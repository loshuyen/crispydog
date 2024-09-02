from .database import pool
import json

def get_published_products(keyword, product_type):
    try:
        result = []
        db = pool.get_connection()
        cursor = db.cursor()
        params = None
        base_statement = "SELECT user.id, product.id, product.name, user.username, price, rating_avg, review_count, thumbnail_url, product_type FROM product INNER JOIN user ON product.owner_id = user.id WHERE status = 1"
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
            user_id, product_id, product_name, user_username, price, rating_avg, review_count, thumbnail_url, product_type_result = item
            result.append({
                "id": product_id,
                "name": product_name,
                "rating_avg": rating_avg,
                "review_count": review_count,
                "price": price,
                "thumbnail_url": thumbnail_url,
                "product_type": product_type_result,
                "owner": {
                    "id": user_id,
                    "username": user_username
                }
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
            "owner": {
                "id": data[9],
                "username": data[7]
            }
        }
        if data[5]:
            result["specification"] = json.loads(data[5])
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

def get_owner_products(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, product.name, price, introduction, specification, image_urls, thumbnail_url, file_size, product_type , status, stock, rating_avg, review_count
            FROM product WHERE owner_id = %s
            ORDER BY created_at DESC;
        """, (user_id, ))
        products = cursor.fetchall()
        if products[0][0] == None:
            return None
        result = []
        for product in products:
            id, product_name, price, introduction, specification, image_urls, thumbnail_url, file_size, product_type , status, stock, rating_avg, review_count = product
            result.append({
                "id": id,
                "name": product_name,
                "price": price,
                "thumbnail": thumbnail_url,
                "product_type": product_type,
                "introduction": introduction,
                "specification": specification,
                "images": image_urls,
                "status": status,
                "stock": stock,
                "rating_avg": rating_avg,
                "review_count": review_count
            })
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def get_product_by_ownername(owner_name):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.id, product.name, price, rating_avg, review_count, introduction, specification, image_urls, user.username, file_size, product_type, thumbnail_url
            FROM product INNER JOIN user ON product.owner_id = user.id
            WHERE status = 1 AND user.username = %s;""", (owner_name, ))
        products = cursor.fetchall()
        result = []
        for product in products:
            product_id, product_name, price, rating_avg, review_count, introduction, specification, image_urls, user_username, file_size, product_type, thumbnail_url = product
            result.append({
                "id": product_id,
                "name": product_name,
                "price": price,
                "product_type": product_type,
                "rating_avg": rating_avg,
                "review_count": review_count,
                "introduction": introduction,
                "specification": specification,
                "images": image_urls,
                "file_size": file_size,
                "thumbnail": thumbnail_url,
            })
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()