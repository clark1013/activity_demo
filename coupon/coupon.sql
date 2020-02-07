CREATE TABLE `coupon` (
  `coupon_id` int(32) NOT NULL AUTO_INCREMENT COMMENT '优惠券id',
  `num` varchar(8) NOT NULL COMMENT '优惠券编码',
  `shop_id` int(11) NOT NULL COMMENT '店铺id',
  `amount` int(11) NOT NULL DEFAULT '0' COMMENT '优惠金额',
  `extend_field` varchar(200) NOT NULL DEFAULT '' COMMENT '扩展字段列表，json串',
  PRIMARY KEY (`coupon_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券表';

CREATE TABLE `coupon_customer` (
  `coupon_customer_id` int(32) NOT NULL AUTO_INCREMENT COMMENT '用户领取记录id',
  `receiver_passport_id` varchar(32) NOT NULL DEFAULT '' COMMENT '用户id',
  `status` tinyint(2) NOT NULL COMMENT '状态，1:未使用，2:已使用',
  PRIMARY KEY (`coupon_customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户领取记录表';

CREATE TABLE `coupon_consume_detail` (
  `coupon_consume_detail_id` int(32) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `coupon_customer_id` int(32) NOT NULL DEFAULT '0' COMMENT '用户领取记录id',
  `order_amount` int(11) NOT NULL DEFAULT '0' COMMENT '订单金额',
  `discount_amount` int(11) NOT NULL DEFAULT '0' COMMENT '实际抵扣金额',
  PRIMARY KEY (`coupon_consume_detail_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券消费记录表'
