from .database import pool

def add_payment(payment, deal_id, user_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO payment 
            (id, user_id, pay_method, deal_id, status, message, rec_trade_id, auth_code, amount, currency, transaction_time) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            payment["number"], user_id, payment["payment"]["pay_method"], deal_id, payment["payment"]["status"], payment["payment"]["message"], payment["payment"]["rec_trade_id"], payment["payment"]["auth_code"], payment["payment"]["amount"], payment["payment"]["currency"], payment["payment"]["transaction_time"]))
        db.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def get_payment(id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT deal_id, user_id, user.username FROM payment INNER JOIN user ON payment.user_id = user.id WHERE payment.id = %s", (id, ))
        deal_id, user_id, username = cursor.fetchall()[0]
        return (deal_id, user_id, username)
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()