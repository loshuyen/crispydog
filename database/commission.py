from .database import pool
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import json

def get_commissions_by_buyer(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT commission.id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission.updated_at, deal.products, deal.success
            FROM commission 
            INNER JOIN deal ON commission.deal_id = deal.id
            INNER JOIN user ON deal.buyer_id = user.id
            WHERE user.id = %s
            ORDER BY commission.updated_at DESC;
        """, (user_id, ))
        data = []
        commissions = cursor.fetchall()
        for commission in commissions:
            commission_id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission_updated_at, products, deal_success = commission
            product_id = json.loads(products)[0]
            cursor.execute("""
                SELECT product.thumbnail_url, product.name, product.price, user.id, user.username
                FROM product 
                INNER JOIN user ON product.owner_id = user.id
                WHERE product.id = %s
            """, (product_id, ))
            product_thumbnail, product_name, product_price, owner_id, owner_username = cursor.fetchall()[0]
            data.append({
                "id": commission_id,
                "photo_url": photo_url,
                "is_accepted": is_accepted,
                "is_paid": is_paid,
                "is_delivered": is_delivered,
                "is_downloaded": is_downloaded,
                "updated_at": commission_updated_at.strftime("%Y-%m-%d %H:%M"),
                "deal": {
                    "id": deal_id,
                    "success": deal_success
                },
                "product": {
                    "id": product_id,
                    "name": product_name,
                    "price": product_price,
                    "thumbnail": product_thumbnail,
                    "owner": {
                        "id": owner_id,
                        "username": owner_username
                    }
                } 
            })
        return data
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def get_commission_by_id_by_buyer(user_id, commission_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT commission.id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission.updated_at, deal.products, deal.success
            FROM commission 
            INNER JOIN deal ON commission.deal_id = deal.id
            INNER JOIN user ON deal.buyer_id = user.id
            WHERE user.id = %s AND commission.id = %s
            ORDER BY commission.updated_at DESC;
        """, (user_id, commission_id))
        data = []
        commissions = cursor.fetchall()
        for commission in commissions:
            commission_id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission_updated_at, products, deal_success = commission
            product_id = json.loads(products)[0]
            cursor.execute("""
                SELECT product.thumbnail_url, product.name, product.price, user.id, user.username
                FROM product 
                INNER JOIN user ON product.owner_id = user.id
                WHERE product.id = %s
            """, (product_id, ))
            product_thumbnail, product_name, product_price, owner_id, owner_username = cursor.fetchall()[0]
            data.append({
                "id": commission_id,
                "photo_url": photo_url,
                "is_accepted": is_accepted,
                "is_paid": is_paid,
                "is_delivered": is_delivered,
                "is_downloaded": is_downloaded,
                "updated_at": commission_updated_at.strftime("%Y-%m-%d %H:%M"),
                "deal": {
                    "id": deal_id,
                    "success": deal_success
                },
                "product": {
                    "id": product_id,
                    "name": product_name,
                    "price": product_price,
                    "thumbnail": product_thumbnail,
                    "owner": {
                        "id": owner_id,
                        "username": owner_username
                    }
                } 
            })
        return data[0]
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def get_commission(commission_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission.updated_at, user.id as buyer_id, user.username as buyer_name, deal.products, deal.success
            FROM commission 
            INNER JOIN deal ON commission.deal_id = deal.id
            INNER JOIN user ON deal.buyer_id = user.id
            WHERE commission.id = %s
            ORDER BY commission.updated_at DESC;
        """, (commission_id, ))
        deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission_updated_at, buyer_id, buyer_name, products, deal_success = cursor.fetchall()[0]
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
            "is_paid": is_paid, 
            "is_delivered": is_delivered, 
            "is_downloaded": is_downloaded,
            "updated_at": commission_updated_at.strftime("%Y-%m-%d %H:%M"),
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

def add_commission(deal_id, photo_url, product_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO commission
            (deal_id, photo_url, product_id) VALUES
            (%s, %s, %s)
        """, (deal_id, photo_url, product_id))
        commission_id = cursor.lastrowid
        db.commit()
        return commission_id
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def update_commission(commission_id, is_accepted=None, is_paid=None, is_delivered=None, is_downloaded=None):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        statement_start = "UPDATE commission SET updated_at = %s,"
        statement_end = "WHERE id = %s"
        statement = None
        params = None
        if is_accepted:
            statement = f"{statement_start} is_accepted = %s {statement_end}"
            params = (datetime.now(tz=timezone(timedelta(hours=8))), is_accepted, commission_id)
        elif is_paid:
            statement = f"{statement_start} is_paid = %s {statement_end}"
            params = (datetime.now(tz=timezone(timedelta(hours=8))), is_paid, commission_id)
        elif is_delivered:
            statement = f"{statement_start} is_delivered = %s {statement_end}"
            params = (datetime.now(tz=timezone(timedelta(hours=8))), is_delivered, commission_id)
        else:
            statement = f"{statement_start} is_downloaded = %s {statement_end}"
            params = (datetime.now(tz=timezone(timedelta(hours=8))), is_downloaded, commission_id)
        cursor.execute(statement, params)
        db.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def update_file_url(commission_id, file_url):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE commission SET file_url = %s, updated_at = %s WHERE id = %s", (file_url, datetime.now(tz=timezone(timedelta(hours=8))), commission_id))
        db.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def get_commissions_by_seller(user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT commission.id, deal.id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission.updated_at, deal.success, user.id, user.username, product.id, product.name, product.price, product.thumbnail_url
            FROM commission 
            INNER JOIN product ON commission.product_id = product.id
            INNER JOIN deal ON deal.id = commission.deal_id
            INNER JOIN user ON deal.buyer_id = user.id
            WHERE product.owner_id = %s
            ORDER BY commission.updated_at DESC;
        """, (user_id, ))
        result = cursor.fetchall()
        data = []
        for item in result:
            commission_id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission_updated_at, deal_success, buyer_id, buyer_username, product_id, product_name, product_price, product_thumbnail_url = item
            data.append({
                "id": commission_id,
                "photo_url": photo_url,
                "file_url": file_url,
                "is_accepted": is_accepted,
                "is_paid": is_paid,
                "is_delivered": is_delivered,
                "is_downloaded": is_downloaded,
                "updated_at": commission_updated_at.strftime("%Y-%m-%d %H:%M"),
                "deal": {
                    "id": deal_id,
                    "success": deal_success
                },
                "product": {
                    "id": product_id,
                    "name": product_name,
                    "price": product_price,
                    "thumbnail": product_thumbnail_url,
                },
                "buyer": {
                    "id": buyer_id,
                    "username": buyer_username
                }
            })
        return data
    except Exception as e:
        return []
    finally:
        cursor.close()
        db.close()

def get_commission_by_id_by_seller(user_id, commission_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT commission.id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission.updated_at, deal.products, deal.success, user.id, user.username
            FROM commission 
            INNER JOIN deal ON commission.deal_id = deal.id
            INNER JOIN user ON deal.buyer_id = user.id
            WHERE commission.id = %s
            ORDER BY commission.updated_at DESC;
        """, (commission_id, ))
        data1 = cursor.fetchall()
        data = []
        for item in data1:
            commission_id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission_updated_at, deal_products, deal_success, buyer_id, buyer_username = item
            product_id = json.loads(deal_products)[0]
            cursor.execute("SELECT product.name, product.price, product.thumbnail_url FROM product WHERE id = %s AND owner_id = %s", (product_id, user_id))
            product_name, product_price, product_thumbnail_url = cursor.fetchall()[0]
            if product_name:
                data.append({
                    "id": commission_id,
                    "photo_url": photo_url,
                    "file_url": file_url,
                    "is_accepted": is_accepted,
                    "is_paid": is_paid,
                    "is_delivered": is_delivered,
                    "is_downloaded": is_downloaded,
                    "updated_at": commission_updated_at.strftime("%Y-%m-%d %H:%M"),
                    "deal": {
                        "id": deal_id,
                        "success": deal_success
                    },
                    "product": {
                        "id": product_id,
                        "name": product_name,
                        "price": product_price,
                        "thumbnail": product_thumbnail_url,
                    },
                    "buyer": {
                        "id": buyer_id,
                        "username": buyer_username
                    }
                })
        return data
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def get_commission_download_by_id_by_buyer(user_id, commission_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT commission.id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission.updated_at, deal.products, deal.success
            FROM commission 
            INNER JOIN deal ON commission.deal_id = deal.id
            INNER JOIN user ON deal.buyer_id = user.id
            WHERE user.id = %s AND commission.id = %s
            ORDER BY commission.updated_at DESC;
        """, (user_id, commission_id))
        data = []
        commissions = cursor.fetchall()
        for commission in commissions:
            commission_id, deal_id ,photo_url, file_url, is_accepted, is_paid, is_delivered, is_downloaded, commission_updated_at, products, deal_success = commission
            product_id = json.loads(products)[0]
            cursor.execute("""
                SELECT product.thumbnail_url, product.name, product.price, user.id, user.username
                FROM product 
                INNER JOIN user ON product.owner_id = user.id
                WHERE product.id = %s
            """, (product_id, ))
            product_thumbnail, product_name, product_price, owner_id, owner_username = cursor.fetchall()[0]
            data.append({
                "commission": {
                    "file_url": file_url,
                    "is_accepted": is_accepted,
                    "is_paid": is_paid,
                    "is_delivered": is_delivered,
                    "is_downloaded": is_downloaded,
                    "updated_at": commission_updated_at.strftime("%Y-%m-%d %H:%M"),
                    "deal": {
                        "id": deal_id,
                        "success": deal_success
                    },
                    "product": {
                        "id": product_id,
                        "name": product_name,
                        "price": product_price,
                        "thumbnail": product_thumbnail,
                        "owner": {
                            "id": owner_id,
                            "username": owner_username
                        }
                    } 
                }
            })
        return data[0]
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()