from .database import pool
from datetime import datetime

def get_all_sales(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.id, product.name, product.price, COUNT(sale.id), product.thumbnail_url, product.status 
            FROM product LEFT JOIN sale ON sale.product_id = product.id
            WHERE product.owner_id = %s
            GROUP BY product.id;""", (user_id, ))
        sales = cursor.fetchall()
        result = []
        for sale in sales:
            product_id, product_name, product_price, sale_count, product_thumbnail, product_status = sale
            result.append({
                "product": {
                    "id": product_id,
                    "name": product_name,
                    "price": product_price,
                    "thumbnail": product_thumbnail,
                    "status": product_status,
                    "sales": sale_count
                }
            })
        return result 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()