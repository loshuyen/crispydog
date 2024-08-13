from .database import pool

def get_all_from_cart(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product_id, product.name, product.price, thumbnail_url
            FROM cart INNER JOIN product ON cart.product_id = product.id
            WHERE cart.user_id = %s
        """, (user_id, ))
        products = cursor.fetchall()
        result = []
        for product in products:
            product_id, product_name, product_price, thumbnail_url = product
            result.append({
                "id": product_id,
                "name": product_name,
                "price": product_price,
                "thumbnail": thumbnail_url
            })
        return result
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        db.close()

def find_product_in_card(user_id, product_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * from cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        product = cursor.fetchall()
        return product
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

def add_product_to_cart(user_id, product_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO cart (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

def remove_product_from_cart(user_id, product_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM cart WHERE user_id = %s and product_id = %s", (user_id, product_id))
        result = cursor.fetchall()[0]
        cursor.execute("DELETE FROM cart WHERE user_id = %s and product_id = %s", (user_id, product_id))
        db.commit()
    except IndexError as e:
        raise e
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def remove_all_product_from_cart(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id, ))
        db.commit()
    except IndexError as e:
        raise e
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()
