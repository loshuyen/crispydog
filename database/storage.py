from .database import pool
from datetime import datetime

def get_all_storage(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT storage.id, product.id, product.name, product.owner_id, user.username, product.thumbnail_url, storage.download_url, storage.created_at
            FROM storage INNER JOIN product ON storage.product_id = product.id
            INNER JOIN user ON product.owner_id = user.id
            WHERE storage.user_id = %s
            ORDER BY storage.created_at DESC;""", (user_id, ))
        products = cursor.fetchall()
        result = []
        for product in products:
            storage_id, product_id, product_name, product_owner_id, user_username, product_thumbnail_url, storage_download_url, storage_created_at = product
            result.append({
                "storage": {
                    "id": storage_id,
                    "created_at": storage_created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "product": {
                        "id": product_id, 
                        "name": product_name,
                        "thumbnail": product_thumbnail_url,
                        "download_url": storage_download_url
                    },
                    "seller": {
                        "id": product_owner_id,
                        "username": user_username
                    }
                }
            })
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()