from .database import pool
from datetime import datetime
from routers import notification
import json

def get_notifications(user_id, is_read = None):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        if not is_read: 
            cursor.execute("""
                SELECT user.username, notification.id, sender_id, receiver_id, message_type, message, is_read, notification.created_at 
                FROM notification INNER JOIN user ON notification.sender_id = user.id 
                WHERE receiver_id = %s 
                ORDER BY notification.created_at DESC
            """, (user_id, ))
        else:
            cursor.execute("""
                SELECT user.username, notification.id, sender_id, receiver_id, message_type, message, is_read, notification.created_at 
                FROM notification INNER JOIN user ON notification.sender_id = user.id 
                WHERE receiver_id = %s and is_read = %s 
                ORDER BY notification.created_at DESC
            """, (user_id, is_read))
        notes = cursor.fetchall()
        result = []
        for note in notes:
            sender_username, notification_id, sender_id, receiver_id, message_type, message, is_read, created_at = note
            result.append({
                "notification": {
                    "id": notification_id,
                    "sender": {
                        "id": sender_id,
                        "username": sender_username
                    },
                    "receiver_id": receiver_id,
                    "message_type": message_type,
                    "message": message,
                    "is_read": is_read,
                    "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            })
        return result 
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        db.close()

async def add_notification(sender_id, sender_name, receiver_id_list, message_type, message = None):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        data = []
        for id in receiver_id_list:
            data.append((sender_id, id, message_type, message))
            await notification.notify_user(id, json.dumps({"sender": sender_name, "message_type": message_type}))
        cursor.executemany("""
            INSERT INTO notification
            (sender_id, receiver_id, message_type, message) VALUES
            (%s, %s ,%s, %s)
        """, data)
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

async def add_single_notification(sender_id, sender_name, receiver_id, message_type, message = None):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO notification
            (sender_id, receiver_id, message_type, message) VALUES
            (%s, %s ,%s, %s)
        """, (sender_id, receiver_id, message_type, message))
        await notification.notify_user(receiver_id, json.dumps({"sender": sender_name, "message_type": message_type}))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

async def mark_all_as_read(receiver_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE notification SET is_read = 1 WHERE receiver_id = %s", (receiver_id, ))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

async def mark_as_read(receiver_id, notification_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE notification SET is_read = 1 WHERE receiver_id = %s AND id = %s", (receiver_id, notification_id))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()

async def mark_as_un_read(receiver_id, notification_id):
    try:
        db = pool.get_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE notification SET is_read = 0 WHERE receiver_id = %s AND id = %s", (receiver_id, notification_id))
        db.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cursor.close()
        db.close()