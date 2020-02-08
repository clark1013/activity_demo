def insert_coupon(session, shop_id, num, amount):
    sql = """
        INSERT INTO `coupon` (`num`, `shop_id`, `amount`)
        VALUES
            ('{}', {}, {});
    """.format(num, shop_id, amount)
    session.execute(sql)
