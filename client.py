import grpc
import demo_pb2, demo_pb2_grpc
import datetime
import time

_HOST = 'localhost'
_PORT = '8080'

def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = demo_pb2_grpc.ActivityStub(channel=conn)
    ctx = demo_pb2.RequestCtx(business="pf", shop_id=105, passport_id=100)
    start = datetime.datetime.now()
    for i in range(100):
        for i in range(100):
            response = client.CreateCoupon(demo_pb2.CreateCouponReq(ctx=ctx, amount=300))
        # print(response.coupon_num)
    print(datetime.datetime.now() - start)

if __name__ == '__main__':
    run()
