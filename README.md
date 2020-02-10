活动平台demo，主要实现了不同业务线调用平台接口，写不同业务线的数据库。
具体的业务代码需要根据需求定制。

# grpc
- 跨语言，可以通过换用技术栈解决性能瓶颈，提高服务的响应速度
- 定义服务接口，见`demo.proto`
- 通过`protobuf`工具，自动生成代码：`demo.pb.go`，`demo_pb2.py`，`deom_pb2_grpc.py`
- 相比于使用HTTP接口，性能更好，客户端开发更加便捷

# 服务端
核心代码如下，`MAP_BUSINESS_SESSION`用以模拟配置中心，配置中心可以维护不同业务身份的关系型数据库，缓存等资源
```
# 连接池映射
MAP_BUSINESS_SESSION = {
    "pf": PF_Session,
    "ls": LS_Session,
}


class ActivityService(demo_pb2_grpc.ActivityServicer):
    def CreateCoupon(self, request, context):
        session = MAP_BUSINESS_SESSION[request.ctx.business]()
```
模型扩展，主要通过`extend_field`存储json来实现不同业务线的自定义扩展
```
CREATE TABLE `coupon` (
  `coupon_id` int(32) NOT NULL AUTO_INCREMENT COMMENT '优惠券id',
  `num` varchar(8) NOT NULL COMMENT '优惠券编码',
  `shop_id` int(11) NOT NULL COMMENT '店铺id',
  `amount` int(11) NOT NULL DEFAULT '0' COMMENT '优惠金额',
  `extend_field` varchar(200) NOT NULL DEFAULT '' COMMENT '扩展字段列表，json串',
  PRIMARY KEY (`coupon_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券表';
```

# 客户端
模拟两条业务线的调用
```
# PF调用
ctx = demo_pb2.RequestCtx(business="pf", shop_id=105, passport_id=100)
response = client.CreateCoupon(demo_pb2.CreateCouponReq(ctx=ctx, amount=300))
print("PF CALL RESULT, coupon_num:", response.coupon_num)
# LS调用
ctx = demo_pb2.RequestCtx(business="ls", shop_id=120, passport_id=340)
response = client.CreateCoupon(demo_pb2.CreateCouponReq(ctx=ctx, amount=600))
print("LS CALL RESULT, coupon_num:", response.coupon_num)
```

# GO语言版本
主要通过goroutine异步写提高并发性能，读接口的并发性能需要增加缓存来提高。通过channel可以限制goroutine的数量避免并发过高占用数据库连接。

# 后续
- 业务抽象，建立真实模型，应用于具体的业务线
- 微服务相关：服务发现、监控、降级、限流、负载均衡等
