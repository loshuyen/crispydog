from .database import pool
from datetime import datetime
import json
from uuid import uuid4

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
                    "id": id,
                    "name": product_name, 
                    "price": product_price, 
                    "owner": {
                        "id": seller_id,
                        "username": seller_name
                    } 
                })
            result.append({
                "id": id,
                "amount": amount,
                "delivery_email": delivery_email,
                "success": success,
                "created_at": updated_at.strftime("%Y-%m-%d %H:%M"),
                "products": product_result
            })
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def get_deal_products_by_id(id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT products FROM deal WHERE id = %s", (id, ))
        products = cursor.fetchall()[0]
        return products[0]
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def add_deal(buyer_id, products, delivery_email, amount, success=None):
    try:
        db = pool.get_connection()
        cursor = db.cursor()

        placeholders = ", ".join(["%s"] * len(products))
        query = f"SELECT * FROM product WHERE id IN ({placeholders})"
        cursor.execute(query, products)
        result = cursor.fetchall()
        if len(result) != len(products):
            raise IndexError
        
        if success != None:
            cursor.execute("""
                INSERT INTO deal
                (buyer_id, amount, products, delivery_email, success) VALUES
                (%s, %s, %s, %s, %s);
            """, (buyer_id, amount, json.dumps(products), delivery_email, success))
        else:
            cursor.execute("""
                INSERT INTO deal
                (buyer_id, amount, products, delivery_email) VALUES
                (%s, %s, %s, %s);
            """, (buyer_id, amount, json.dumps(products), delivery_email))
        deal_id = cursor.lastrowid
        db.commit()
        return deal_id
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def mark_as_success(deal_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE deal SET success = 1 WHERE id = %s", (deal_id, ))
        db.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def calculate_amount(products):
    try:
        db = pool.get_connection()
        cursor = db.cursor()

        placeholders = ", ".join(["%s"] * len(products))
        query = f"SELECT SUM(price) FROM product WHERE id IN ({placeholders})"
        cursor.execute(query, products)
        result = cursor.fetchall()[0][0]
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def add_sale_records(deal_id, buyer_id, products):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        data = []
        for product_id in products:
            download_endpoint = str(uuid4())
            data.append((deal_id, buyer_id, product_id, download_endpoint))
        cursor.executemany("""
            INSERT INTO sale 
            (deal_id, buyer_id, product_id, download_endpoint) VALUES
            (%s, %s, %s, %s)
        """, data)
        db.commit()
        return deal_id
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def update_seller_savings(products):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        pairs = []
        for product_id in products:
            cursor.execute("""
                SELECT user.id, product.price
                FROM product INNER JOIN user ON product.owner_id = user.id
                WHERE product.id = %s
            """, (product_id, ))
            pairs.append(cursor.fetchone())
        db.commit()
        
        db.start_transaction()
        for pair in pairs:
            user_id, product_price = pair
            cursor.execute("SELECT savings FROM user WHERE id = %s FOR UPDATE", (user_id, ))
            savings = cursor.fetchone()[0]
            cursor.execute("UPDATE user SET savings = %s WHERE id = %s", (savings + product_price, user_id))
        db.commit()
            
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()

def transfer_savings(products, buyer_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        pairs = []
        for product_id in products:
            cursor.execute("""
                SELECT user.id, product.price
                FROM product INNER JOIN user ON product.owner_id = user.id
                WHERE product.id = %s
            """, (product_id, ))
            pairs.append(cursor.fetchone())
        db.commit()
        
        db.start_transaction()
        for pair in pairs:
            owner_id, product_price = pair
            cursor.execute("SELECT savings FROM user WHERE id = %s FOR UPDATE", (buyer_id, ))
            buyer_savings = cursor.fetchall()[0][0]
            if buyer_savings < product_price:
                raise Exception("Not enough savings.")
            cursor.execute("UPDATE user SET savings = %s WHERE id = %s", (buyer_savings - product_price, buyer_id))
            cursor.execute("SELECT savings FROM user WHERE id = %s FOR UPDATE", (owner_id, ))
            owner_savings = cursor.fetchall()[0][0]
            cursor.execute("UPDATE user SET savings = %s WHERE id = %s", (owner_savings + product_price, owner_id))
        db.commit()
            
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()