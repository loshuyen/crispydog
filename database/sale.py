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

def get_sales(user_id, product_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT product.id, product.name, product.price, product.thumbnail_url, product.status, user.username, user.id, sale.id, sale.created_at, review.id, review.rating, review.content, review.updated_at 
            FROM product 
            INNER JOIN sale ON sale.product_id = product.id
            INNER JOIN user ON sale.buyer_id = user.id
            INNER JOIN review ON review.product_id = product.id
            WHERE product.owner_id = %s AND product.id = %s;""", (user_id, product_id))
        sales = cursor.fetchall()
        result = []
        for sale in sales:
            product_id, product_name, product_price, product_thumbnail_url, product_status, buyer_username, buyer_id, sale_id, sale_created_at, review_id, review_rating, review_content, review_updated_at = sale
            result.append({
                "product": {
                    "id": product_id,
                    "name": product_name,
                    "price": product_price,
                    "thumbnail": product_thumbnail_url,
                    "status": product_status,
                },
                "buyer": {
                    "id": buyer_id,
                    "name": buyer_username,
                },
                "sale": {
                    "id": sale_id,
                    "created_at": sale_created_at.strftime("%Y-%m-%d %H:%M:%S")
                },
                "review": {
                    "id": review_id,
                    "rating": review_rating,
                    "content": review_content,
                    "updated_at": review_updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            })
        return result 
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()