from .database import pool
from datetime import datetime

def get_reviews(product_id, page):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT username, rating, content, review.updated_at, review.id, user.id 
            FROM review INNER JOIN user ON reviewer_id = user.id
            WHERE review.product_id = %s
            ORDER BY review.updated_at DESC
            LIMIT 11 OFFSET %s;""", (product_id, page * 10))
        reviews = cursor.fetchall()
        next_page = None
        if len(reviews) > 10:
            next_page = page + 1
        result = []
        for i in range(min(10, len(reviews))):
            result.append({
                "review": {
                    "id":reviews[i][4],
                    "rating":reviews[i][1],
                    "content":reviews[i][2],
                    "updated_at":reviews[i][3].strftime("%Y-%m-%d %H:%M:%S"),
                    "reviewer":{
                        "id":reviews[i][5],
                        "name":reviews[i][0]
                    }
                }
            })
        return {"next_page": next_page, "data": result}
    except Exception as e:
        print(e)
        return {"next_page": None, "data": None}
    finally:
        cursor.close()
        db.close()

def add_review(reviewer_id, rating, content, product_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO review
            (reviewer_id, rating, content, product_id) VALUES
            (%s, %s, %s, %s);
            """, (reviewer_id, rating, content, product_id))
        db.commit()
        
        cursor.execute("SELECT rating_avg, review_count FROM product WHERE id = %s", (product_id, ))
        rating_avg, review_count = cursor.fetchall()[0]
        new_rating_avg = (rating_avg * review_count + rating) / (review_count + 1)
        new_review_count = review_count + 1
        
        cursor.execute("""
            UPDATE product SET rating_avg = %s, review_count = %s
            WHERE id = %s;""", (new_rating_avg, new_review_count, product_id))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

def get_review(product_id, user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM review WHERE product_id = %s and reviewer_id = %s", (product_id, user_id))
        review = cursor.fetchall()[0]
        return review[0]
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        db.close()

def update_review(rating, content, product_id, review_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT review.rating, rating_avg, review_count 
            FROM review INNER JOIN product ON review.product_id = product.id
            WHERE review.id = %s""", (review_id, ))
        old_rating, rating_avg, review_count = cursor.fetchall()[0]
        new_rating_avg = (rating_avg * review_count - old_rating + rating) / review_count
        
        cursor.execute("UPDATE product SET rating_avg = %s WHERE id = %s;", (new_rating_avg, product_id))
        db.commit()

        cursor.execute("UPDATE review SET rating = %s, content = %s, updated_at = %s WHERE id = %s;", (rating, content, datetime.now(), review_id))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()