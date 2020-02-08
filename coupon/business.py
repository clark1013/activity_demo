import uuid
from .data_access import insert_coupon


def create_coupon(session, shop_id, amount):
    num = str(uuid.uuid4())[:8]
    insert_coupon(session, shop_id, num, amount)
    session.commit()
    return num
