import uuid
from .data_access import insert_coupon


def create_coupon(conn, shop_id, amount):
    cursor = conn.cursor()
    num = str(uuid.uuid4())[:8]
    insert_coupon(cursor, shop_id, num, amount)
    cursor.close()
    conn.commit()
    return num
