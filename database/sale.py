from .database import pool
from datetime import datetime

def get_all_sales(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT sale.id, sale.buyer_id, sale.created_at, user.username, product.id, product.name, product.price, product.thumbnail_url
            FROM product INNER JOIN sale ON sale.product_id = product.id
            INNER JOIN user ON sale.buyer_id = user.id
            WHERE product.owner_id = %s
            ORDER BY sale.created_at DESC;
        """, (user_id, ))
        sales = cursor.fetchall()
        result = []
        for sale in sales:
            sale_id, sale_buyer_id, sale_created_at, user_username, product_id, product_name, product_price, product_thumbnail_url = sale
            result.append({
                "id": sale_id,
                "created_at": sale_created_at.strftime("%Y-%m-%d %H:%M"),
                "buyer": {
                    "id": sale_buyer_id,
                    "username": user_username
                },
                "product": {
                    "id": product_id,
                    "name": product_name,
                    "price": product_price,
                    "thumbnail": product_thumbnail_url,
                }
            })
        return result 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def get_sales(user_id, product_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT sale.id, sale.buyer_id, sale.created_at, user.username
            FROM sale
            INNER JOIN user ON sale.buyer_id = user.id
            INNER JOIN product ON sale.product_id = product.id
            WHERE product.owner_id = %s AND sale.product_id = %s
            ORDER BY sale.created_at DESC;
        """, (user_id, product_id))
        sales = cursor.fetchall()
        sales_result = []
        for sale in sales:
            sale_id, sale_buyer_id, sale_created_at, user_username = sale
            sales_result.append({
                "id": sale_id,
                "created_at": sale_created_at.strftime("%Y-%m-%d %H:%M"),
                "buyer": {
                    "id": sale_buyer_id,
                    "username": user_username
                }
            })
        cursor.execute("""
            SELECT product.id, COUNT(sale.id), product.name, product.price, product.thumbnail_url,product.status
            FROM sale INNER JOIN product ON sale.product_id = product.id
            WHERE product.owner_id = %s AND product.id = %s
            ORDER BY sale.created_at DESC;
        """, (user_id, product_id))
        product = cursor.fetchall()[0]
        if product[0] == None:
            return None
        id, sales_count, product_name, product_price, product_thumbnail_url, product_status = product
        result = {
            "product": {
                "id": product_id,
                "name": product_name,
                "price": product_price,
                "thumbnail": product_thumbnail_url,
                "status": product_status,
                "sales_count": sales_count,
                "sales": sales_result
            }
        }
        return result 
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()