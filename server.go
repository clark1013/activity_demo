package main

import (
    "log"
    "net"
    "fmt"

    pb "github.com/clark1013/activity_demo/pb"
    "golang.org/x/net/context"
    "google.golang.org/grpc"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)

const (
    port = ":8080"
)

var DB, _ = sql.Open("mysql", "local:senguo_mysql@tcp(127.0.0.1:3308)/pfdb")
var ch = make(chan int, 100)

type server struct{}

func insertDb(db *sql.DB) {
    _, err := db.Exec("INSERT INTO `coupon` (`num`, `shop_id`, `amount`) VALUES (?,?,?)", "122", 100, 300)
    if err != nil {
        panic(err)
    }
    _ = <- ch
}

func (s *server) CreateCoupon(ctx context.Context, in *pb.CreateCouponReq) (*pb.CreateCouponResp, error) {
    ch <- 1
    go insertDb(DB)
    return &pb.CreateCouponResp{CouponNum: "Hello"}, nil
}

func (s *server) SendCoupon(ctx context.Context, in *pb.SendCouponReq) (*pb.SendCouponResp, error) {
    return &pb.SendCouponResp{}, nil
}

func (s *server) UseCoupon(ctx context.Context, in *pb.UseCouponReq) (*pb.UseCouponResp, error) {
    return &pb.UseCouponResp{}, nil
}

func main() {
    lis, err := net.Listen("tcp", port)
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    s := grpc.NewServer()
    pb.RegisterActivityServer(s, &server{})
    fmt.Println("init server success")
    s.Serve(lis)
}
