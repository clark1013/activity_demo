import grpc
import demo_pb2, demo_pb2_grpc


_HOST = "localhost"
_PORT = "8080"


def run():
    conn = grpc.insecure_channel(_HOST + ":" + _PORT)
    client = demo_pb2_grpc.ActivityStub(channel=conn)
    # PF调用
    ctx = demo_pb2.RequestCtx(business="pf", shop_id=105, passport_id=100)
    response = client.CreateCoupon(demo_pb2.CreateCouponReq(ctx=ctx, amount=300))
    print("PF CALL RESULT, coupon_num:", response.coupon_num)
    # LS调用
    ctx = demo_pb2.RequestCtx(business="ls", shop_id=120, passport_id=340)
    response = client.CreateCoupon(demo_pb2.CreateCouponReq(ctx=ctx, amount=600))
    print("LS CALL RESULT, coupon_num:", response.coupon_num)


if __name__ == "__main__":
    run()
