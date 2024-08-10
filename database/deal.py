from .database import pool
from datetime import datetime
import json

def get_all_deals(user_id, success):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        statement = "SELECT * FROM deal WHERE buyer_id = %s"
        params = (user_id, )
        if success != None:
            statement = "SELECT * FROM deal WHERE buyer_id = %s and success = %s"
            params = (user_id, success)
        statement += " ORDER BY updated_at DESC"
        cursor.execute(statement, params)
        deals = cursor.fetchall()
        result = []
        for deal in deals:
            id, buyer_id, amount, products, delivery_email, success, created_at, updated_at = deal
            product_result = []
            for id in json.loads(products):
                cursor.execute("SELECT product.name, product.price, user.username, user.id FROM product INNER JOIN user ON product.owner_id = user.id WHERE product.id = %s", (id, ))
                product_name, product_price, seller_name, seller_id = cursor.fetchall()[0]
                product_result.append({
                    "product_id": id,
                    "product_name": product_name, 
                    "product_price": product_price, 
                    "seller_id": seller_id,
                    "seller_name": seller_name
                })
            result.append({
                "deal": {
                    "id": id,
                    "amount": amount,
                    "delivery_email": delivery_email,
                    "success": success,
                    "created_at": updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "products": product_result
                }
            })
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def add_deal(buyer_id, products, delivery_email, amount):
    try:
        db = pool.get_connection()
        cursor = db.cursor()

        placeholders = ", ".join(["%s"] * len(products))
        query = f"SELECT * FROM product WHERE id IN ({placeholders})"
        cursor.execute(query, products)
        result = cursor.fetchall()
        if len(result) != len(products):
            raise IndexError
        
        cursor.execute("""
            INSERT INTO deal
            (buyer_id, amount, products, delivery_email) VALUES
            (%s, %s, %s, %s);""", 
            (buyer_id, amount, json.dumps(products), delivery_email))
        db.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()