def insert_coupon(cursor, shop_id, num, amount):
    sql = """
        INSERT INTO `coupon` (`num`, `shop_id`, `amount`)
        VALUES
            ('{}', {}, {});
    """.format(num, shop_id, amount)
    cursor.execute(sql)
