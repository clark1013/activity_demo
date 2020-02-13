""" 毛利模型, 放在这里用于备份 """
import copy
from collections import defaultdict
from prettytable import PrettyTable
from types import FunctionType


def demo():
    """ 基本模型的输出示例 """
    x = PrettyTable()

    x.field_names = ["日期", "采购的商品", "商品销售成本", "存货金额"]
    x.add_row(["8月1日", "期初余额", "", "10*91元=910元"])
    x.add_row(["8月3日", "15*106元=1590元", "", "10*91元+15*106元=2500元"])
    x.add_row(["8月14日", "", "10*91元+10*106元=1970元", "5*106元=530元"])
    x.add_row(["8月17日", "20*115元=2300元", "", "5*106元+20*115元=2830元"])
    x.add_row(["8月28日", "10*119元=1190元", "", "5*106元+20*115元+10*119元=4020元"])
    x.add_row(["8月31日", "", "5*106元+18*115元=2600元", "2*115元+10*119元=1420元"])
    print(x)


def build_segment_func(warehouse_produce_moves):
    """ 构建成本分段函数 """
    total_quantity = 0
    total_amount = 0
    f_str = "def foo(q):"
    if not warehouse_produce_moves:
        f_str += "\n\treturn 0"
    for i, m in enumerate(warehouse_produce_moves):
        if i == 0:
            f_str += "\n\tif q <= {m_quantity}:\n\t\treturn q * ({m_amount} / {m_quantity})".format(
                m_quantity=m.quantity, m_amount=m.amount,
            )
        elif 0 < i < len(warehouse_produce_moves) - 1:
            f_str += "\n\telif {total_quantity} < q <= {total_quantity} + {m_quantity}:\n\t\treturn {total_amount} + (q - {total_quantity}) * ({m_amount} / {m_quantity})".format(
                total_quantity=total_quantity,
                total_amount=total_amount,
                m_quantity=m.quantity,
                m_amount=m.amount,
            )
        if i == len(warehouse_produce_moves) - 1:
            f_str += "\n\telse:\n\t\treturn {total_amount} + (q - {total_quantity}) * ({m_amount} / {m_quantity})".format(
                total_quantity=total_quantity,
                total_amount=total_amount,
                m_quantity=m.quantity,
                m_amount=m.amount,
            )
        total_quantity += m.quantity
        total_amount += m.amount
    f_code = compile(f_str, "<string>", "exec")
    f = FunctionType(f_code.co_consts[0], globals(), "foo")
    return f


class Warehouse:
    """ 仓库 """

    def __init__(self):
        self.stock_moves = []  # 仓库发生的库存变动
        self.quantity = 0  # 存货量
        self.amount = 0  # 存货金额
        self.inventorys = []  # 存货详情

    def purchase_in(self, stock_move):
        """ 采购入库 """
        self.stock_moves.append(stock_move)
        self.inventorys.append(copy.deepcopy(stock_move))
        self.quantity += stock_move.quantity
        self.amount += stock_move.amount

    def sale_out(self, stock_move):
        """ 销售出库 """
        the_quanity = -stock_move.quantity
        while the_quanity > 0:
            inventory = self.inventorys.pop(0)
            consume_quantity = min(the_quanity, inventory.quantity)
            consume_amount = inventory.amount / inventory.quantity * consume_quantity
            stock_move.amount -= consume_amount
            inventory.quantity -= consume_quantity
            inventory.amount -= consume_amount
            the_quanity -= consume_quantity
            if inventory.quantity > 0:
                self.inventorys.insert(0, inventory)
        self.stock_moves.append(stock_move)
        self.quantity += stock_move.quantity
        self.amount += stock_move.amount

    def sum_stock_moves(self):
        """ 对于库存移动进行求和 """
        result = StockMove(0)
        for s in self.stock_moves:
            result.quantity += s.quantity
            result.amount += s.amount
        return result


class SegmentFunction:
    """ 成本分段函数 """

    def __init__(self):
        self._purchase_stock_moves = []

    def build(self, stock_moves):
        self._purchase_stock_moves = stock_moves

    def purchase_cost(self, quantity):
        # 没有入库按照零成本计算
        if not self._purchase_stock_moves:
            return 0
        pt_amount = 0
        pt_quantity = 0
        for p in self._purchase_stock_moves:
            # 未超卖的库存成本直接返回
            if p.quantity + pt_quantity > quantity:
                return pt_amount + (p.amount / p.quantity) * (quantity - pt_quantity)
            else:
                pt_amount += p.amount
                pt_quantity += p.quantity
        # 超卖部分按照最近一次采购计算
        recent_purchase = self._purchase_stock_moves[-1]
        return pt_amount + (recent_purchase.amount / recent_purchase.quantity) * (
            quantity - pt_quantity
        )

    def sale_cost(self, quantity):
        return -self.purchase_cost(quantity)


class SegmentFunctionV2:
    def __init__(self):
        self.f = build_segment_func([])

    def build(self, func):
        self.f = func

    def purchase_cost(self, quantity):
        return self.f(quantity)

    def sale_cost(self, quantity):
        return -self.f(quantity)


class WarehouseV2:
    """ 仓库 """

    def __init__(self):
        self.stock_moves = []  # 仓库发生的库存变动
        self.purchase_stock_moves = []
        self.segf = SegmentFunctionV2()
        self.purchase_quantity = 0
        self.purchase_amount = 0
        self.sale_quantity = 0
        self.sale_amount = 0

    @property
    def quantity(self):
        return self.purchase_quantity - self.sale_quantity

    @property
    def amount(self):
        return self.purchase_amount + self.sale_amount

    @property
    def should_recal(self):
        return bool(self.quantity < 0)

    def purchase_in(self, stock_move, recal=False):
        """ 采购入库 """
        # 入库前记录是否需要重算
        should_recal = self.should_recal
        self.stock_moves.append(stock_move)
        self.purchase_quantity += stock_move.quantity
        self.purchase_amount += stock_move.amount
        self.purchase_stock_moves.append(stock_move)
        func = build_segment_func(self.purchase_stock_moves)
        self.segf.build(func)
        if should_recal:
            self.recalculate()

    def sale_out(self, stock_move):
        """ 销售出库 """
        stock_move.amount = self.segf.sale_cost(
            self.sale_quantity - stock_move.quantity
        ) - self.segf.sale_cost(self.sale_quantity)
        self.sale_quantity -= stock_move.quantity
        self.sale_amount += stock_move.amount
        self.stock_moves.append(stock_move)

    def recalculate(self):
        self.sale_quantity = 0
        self.sale_amount = 0
        for s in self.stock_moves:
            if s.move_type != "SALE":
                continue
            s.amount = self.segf.sale_cost(
                self.sale_quantity - s.quantity
            ) - self.segf.sale_cost(self.sale_quantity)
            self.sale_quantity -= s.quantity
            self.sale_amount += s.amount

    def sum_stock_moves(self):
        """ 对于库存移动进行求和 """
        result = StockMove(0)
        for s in self.stock_moves:
            result.quantity += s.quantity
            result.amount += s.amount
        return result


class StockMove:
    """ 库存变动 """

    def __init__(self, quantity, amount=0):
        self.quantity = quantity
        self.amount = amount

    def to_warehouse(self, warehouse):
        """ 库存移动到仓库 """
        raise NotImplementedError


class PurchaseInStockMove(StockMove):
    """ 采购入库库存变动 """

    move_type = "PURCHASE"

    def to_warehouse(self, warehouse):
        warehouse.purchase_in(self)


class SaleOutStockMove(StockMove):
    """ 销售出库库存变动 """

    move_type = "SALE"

    def to_warehouse(self, warehouse):
        warehouse.sale_out(self)


def test_basic_model():
    """ 最最基本的模型测试，先入库再销售且余量足够 """
    warehouse = WarehouseV2()

    s1 = PurchaseInStockMove(10, amount=910)
    s1.to_warehouse(warehouse)

    s2 = PurchaseInStockMove(15, amount=1590)
    s2.to_warehouse(warehouse)

    s3 = SaleOutStockMove(-20)
    s3.to_warehouse(warehouse)

    s4 = PurchaseInStockMove(20, amount=2300)
    s4.to_warehouse(warehouse)

    s5 = PurchaseInStockMove(10, amount=1190)
    s5.to_warehouse(warehouse)

    s6 = SaleOutStockMove(-23)
    s6.to_warehouse(warehouse)

    assert warehouse.amount == 1420

    r = warehouse.sum_stock_moves()
    assert warehouse.quantity == r.quantity
    assert warehouse.amount == r.amount


def test_sale_first_storage_full():
    """ 先销售再入库的，余量充足的场景 """
    warehouse = WarehouseV2()

    s6 = SaleOutStockMove(-23)
    s6.to_warehouse(warehouse)

    s3 = SaleOutStockMove(-20)
    s3.to_warehouse(warehouse)

    s1 = PurchaseInStockMove(10, amount=910)
    s1.to_warehouse(warehouse)

    s2 = PurchaseInStockMove(15, amount=1590)
    s2.to_warehouse(warehouse)

    s4 = PurchaseInStockMove(20, amount=2300)
    s4.to_warehouse(warehouse)

    s5 = PurchaseInStockMove(10, amount=1190)
    s5.to_warehouse(warehouse)

    assert warehouse.amount == 1420

    r = warehouse.sum_stock_moves()
    assert warehouse.quantity == r.quantity
    assert warehouse.amount == r.amount


if __name__ == "__main__":
    demo()
    test_basic_model()
