from .database import pool
from datetime import datetime
import json

def get_commission(commission_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT deal_id ,photo_url, file_url, is_accepted, is_paied, is_delivered, is_downloaded, commission.updated_at, user.id as buyer_id, user.username as buyer_name, deal.products, deal.success
            FROM commission 
            INNER JOIN deal ON commission.deal_id = deal.id
            INNER JOIN user ON deal.buyer_id = user.id
            WHERE commission.id = %s
        """, (commission_id, ))
        deal_id ,photo_url, file_url, is_accepted, is_paied, is_delivered, is_downloaded, commission_updated_at, buyer_id, buyer_name, products, deal_success = cursor.fetchall()[0]
        product_id_list = json.loads(products)
        product_id = product_id_list[0]
        cursor.execute("""
            SELECT user.id, user.username, product.id, product.name, product.price
            FROM product 
            INNER JOIN user ON product.owner_id = user.id
            WHERE product.id = %s
        """, (product_id, ))
        owner_id, owner_username, product_id, product_name, product_price = cursor.fetchall()[0]
        return {
            "photo_url": photo_url,
            "file_url": file_url, 
            "is_accepted": is_accepted, 
            "is_paied": is_paied, 
            "is_delivered": is_delivered, 
            "is_downloaded": is_downloaded,
            "updated_at": commission_updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "deal": {
                "id": deal_id,
                "success": deal_success
            },
            "buyer": {
                "id": buyer_id,
                "username": buyer_name
            },
            "owner": {
                "id": owner_id,
                "username": owner_username
            },
            "product": {
                "id": product_id,
                "name": product_name,
                "price": product_price
            }
        }
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def add_commission(deal_id, photo_url):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO commission
            (deal_id, photo_url) VALUES
            (%s, %s)
        """, (deal_id, photo_url))
        deal_id = cursor.lastrowid
        db.commit()
        return deal_id
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def update_commission(commission_id, is_accepted=None, is_paied=None, is_delivered=None, is_downloaded=None):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        statement_start = "UPDATE commission SET updated_at = %s,"
        statement_end = "WHERE id = %s"
        statement = None
        params = None
        if is_accepted:
            statement = f"{statement_start} is_accepted = %s {statement_end}"
            params = (datetime.now(), is_accepted, commission_id)
        elif is_paied:
            statement = f"{statement_start} is_paied = %s {statement_end}"
            params = (datetime.now(), is_paied, commission_id)
        elif is_delivered:
            statement = f"{statement_start} is_delivered = %s {statement_end}"
            params = (datetime.now(), is_delivered, commission_id)
        else:
            statement = f"{statement_start} is_downloaded = %s {statement_end}"
            params = (datetime.now(), is_downloaded, commission_id)
        cursor.execute(statement, params)
        db.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()