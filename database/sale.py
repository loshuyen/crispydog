from .database import pool
from datetime import datetime

def get_all_sales(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.id, product.name, SUM(amount), COUNT(product.id) 
            FROM sale INNER JOIN product ON sale.product_id = product.id
            WHERE sale.seller_id = %s
            GROUP BY product.id;""", (user_id, ))
        sales = cursor.fetchall()
        result = []
        for sale in sales:
            product_id, product_name, revenue, sale_count = sale
            result.append({
                "product": {
                    "id": product_id,
                    "name": product_name,
                    "revenue": int(revenue),
                    "sales": sale_count
                }
            })
        return result 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()