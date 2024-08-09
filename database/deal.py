from .database import pool
from datetime import datetime

def get_all_deals(user_id, role, product_id, success):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        statement = None
        query_parameter = (user_id, )
        if role == 0:
            statement = """
                SELECT deal.id, seller_id, product_id, amount, delivery_email, download_url, success, deal.updated_at, user.username, source_url 
                FROM deal INNER JOIN user 
                ON deal.seller_id = user.id WHERE buyer_id = %s"""
        if role == 1:
            statement = """
                SELECT deal.id, buyer_id, product_id, amount, delivery_email, download_url, success, deal.updated_at, user.username, source_url
                FROM deal INNER JOIN user 
                ON deal.buyer_id = user.id WHERE seller_id = %s"""
        if product_id and success != None:
            statement += " and product_id = %s and success = %s"
            query_parameter = (user_id, product_id, success)
        if product_id and success == None:
            statement += " and product_id = %s"
            query_parameter = (user_id, product_id)
        if success != None and not product_id:
            statement += " and success = %s"
            query_parameter = (user_id, success)
        statement += " ORDER BY deal.updated_at DESC;"
        cursor.execute(statement, query_parameter)
        deals = cursor.fetchall()
        result = []
        for deal in deals:
            dic = {
                "deal": {
                    "id": deal[0],
                    "amount": deal[3],
                    "delivery_email": deal[4],
                    "success": deal[6],
                    "updated_at": deal[7].strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            if role == 0:
                dic["seller"] = {
                    "id": deal[1],
                    "name": deal[8]
                }
                dic["product"] = {
                    "id": deal[2],
                    "download_url": deal[5], 
                }
            if role == 1:
                dic["buyer"] = {
                    "id": deal[1],
                    "name": deal[8]
                }
                dic["product"] = {
                    "id": deal[2],
                    "source_url": deal[9], 
                }
            result.append(dic)
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def add_deal(buyer_id, product_id, delivery_email):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT owner_id, price, source_url FROM product WHERE id = %s", (product_id, ))
        owner_id, price, source_url = cursor.fetchall()[0]

        cursor.execute("""
            INSERT INTO deal
            (buyer_id, seller_id, product_id, amount, delivery_email, source_url) VALUES
            (%s, %s, %s, %s, %s, %s);""", 
            (buyer_id, owner_id, product_id, price, delivery_email, source_url))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()