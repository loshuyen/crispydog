from .database import pool
from datetime import datetime
from zoneinfo import ZoneInfo

def get_all_storage(user_id, product_id, product_type):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        if product_id == None and product_type == None:
            cursor.execute("""
                SELECT product.product_type, product.file_type, product.file_size, product.id, product.name, product.price, product.owner_id, user.username, product.thumbnail_url, sale.download_endpoint, sale.created_at
                FROM sale INNER JOIN product ON sale.product_id = product.id
                INNER JOIN user ON product.owner_id = user.id
                WHERE sale.buyer_id = %s
                ORDER BY sale.created_at DESC;""", (user_id, ))
        elif product_id != None and product_type == None:
            cursor.execute("""
                SELECT product.product_type, product.file_type, product.file_size, product.id, product.name, product.price, product.owner_id, user.username, product.thumbnail_url, sale.download_endpoint, sale.created_at
                FROM sale INNER JOIN product ON sale.product_id = product.id
                INNER JOIN user ON product.owner_id = user.id
                WHERE sale.buyer_id = %s AND product.id = %s
                ORDER BY sale.created_at DESC;""", (user_id, product_id))
        elif product_id == None and product_type != None:
            cursor.execute("""
                SELECT product.product_type, product.file_type, product.file_size, product.id, product.name, product.price, product.owner_id, user.username, product.thumbnail_url, sale.download_endpoint, sale.created_at
                FROM sale INNER JOIN product ON sale.product_id = product.id
                INNER JOIN user ON product.owner_id = user.id
                WHERE sale.buyer_id = %s AND product.product_type = %s
                ORDER BY sale.created_at DESC;""", (user_id, product_type))
        else:
            cursor.execute("""
                SELECT product.product_type, product.file_type, product.file_size, product.id, product.name, product.price, product.owner_id, user.username, product.thumbnail_url, sale.download_endpoint, sale.created_at
                FROM sale INNER JOIN product ON sale.product_id = product.id
                INNER JOIN user ON product.owner_id = user.id
                WHERE sale.buyer_id = %s AND product.id = %s AND product.product_type = %s
                ORDER BY sale.created_at DESC;""", (user_id, product_id, product_type))
        products = cursor.fetchall()
        result = []
        for product in products:
            product_type, product_file_type, product_file_size, product_id, product_name, product_price,product_owner_id, user_username, product_thumbnail_url, sale_download_endpoint, sale_created_at = product
            result.append({
                "download_endpoint": sale_download_endpoint,
                "file_type": product_file_type,
                "file_size": product_file_size,
                "created_at": sale_created_at.astimezone(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M"),
                "product": {
                    "id": product_id, 
                    "name": product_name,
                    "price": product_price,
                    "thumbnail": product_thumbnail_url,
                    "product_type": product_type,
                    "owner": {
                        "id": product_owner_id,
                        "username": user_username
                    }
                },
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