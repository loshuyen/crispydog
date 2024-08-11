from .database import pool
from datetime import datetime

def get_all_storage(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.id, product.name, product.owner_id, user.username, product.thumbnail_url, sale.download_endpoint, sale.created_at
            FROM sale INNER JOIN product ON sale.product_id = product.id
            INNER JOIN user ON product.owner_id = user.id
            WHERE sale.buyer_id = %s
            ORDER BY sale.created_at DESC;""", (user_id, ))
        products = cursor.fetchall()
        result = []
        for product in products:
            product_id, product_name, product_owner_id, user_username, product_thumbnail_url, sale_download_endpoint, sale_created_at = product
            result.append({
                "storage": {
                    "product": {
                        "id": product_id, 
                        "name": product_name,
                        "thumbnail": product_thumbnail_url,
                        "download_endpoint": sale_download_endpoint,
                        "seller": {
                            "id": product_owner_id,
                            "username": user_username
                        }
                    },
                    "created_at": sale_created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            })
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def get_source_url(user_id, download_endpoint):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.source_url
            FROM sale INNER JOIN product ON sale.product_id = product.id
            WHERE sale.buyer_id = %s and sale.download_endpoint = %s;
        """, (user_id, download_endpoint))
        source_url = cursor.fetchall()[0][0]
        return source_url
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()