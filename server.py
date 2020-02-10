import grpc
import time
from concurrent import futures
import demo_pb2, demo_pb2_grpc
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from coupon.business import create_coupon

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = "localhost"
_PORT = "8080"
# PF数据库
pf_engine = create_engine(
    "mysql+mysqlconnector://local:senguo_mysql@localhost:3308/pfdb?charset=utf8",
    pool_size=20,
    max_overflow=100,
    pool_recycle=7200,
    echo=False,  # 调试模式，开启后可输出所有查询语句
)
PF_Session = sessionmaker(bind=pf_engine)
# LS数据库
ls_engine = create_engine(
    "mysql+mysqlconnector://local:senguo_mysql@localhost:3308/lsdb?charset=utf8",
    pool_size=20,
    max_overflow=100,
    pool_recycle=7200,
    echo=False,  # 调试模式，开启后可输出所有查询语句
)
LS_Session = sessionmaker(bind=ls_engine)
# 连接池映射
MAP_BUSINESS_SESSION = {
    "pf": PF_Session,
    "ls": LS_Session,
}


class ActivityService(demo_pb2_grpc.ActivityServicer):
    def CreateCoupon(self, request, context):
        session = MAP_BUSINESS_SESSION[request.ctx.business]()
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
    server.add_insecure_port(_HOST + ":" + _PORT)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
