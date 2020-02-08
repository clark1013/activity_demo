import grpc
import time
from concurrent import futures
import demo_pb2, demo_pb2_grpc
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from coupon.business import create_coupon

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '8080'

# conn = pymysql.connect(host="localhost", port=3308, user="local", password="senguo_mysql", database="pfdb", charset="utf8mb4")
engine = create_engine(
    "mysql+mysqlconnector://local:senguo_mysql@localhost:3308/pfdb?charset=utf8",
    pool_size    = 20,
    max_overflow = 100,
    pool_recycle = 7200,
    echo         = False  # 调试模式，开启后可输出所有查询语句
)
# MapBase = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)


class ActivityService(demo_pb2_grpc.ActivityServicer):

    def CreateCoupon(self, request, context):
        # print(request.ctx.business)
        session = DBSession()
        num = create_coupon(session, request.ctx.shop_id, request.amount)
        session.close()
        return demo_pb2.CreateCouponResp(coupon_num=num)

    def SendCoupon(self, request, context):
        pass

    def UseCoupon(self, request, context):
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    demo_pb2_grpc.add_ActivityServicer_to_server(ActivityService(), server)
    server.add_insecure_port(_HOST + ':' + _PORT)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
