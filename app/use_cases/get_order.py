from ..exceptions.order import OrderNotFoundError
from ..ports import UnitOfWorkProtocol
from ..schemas import Order


class GetOrderUseCase:
    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(self, order_id: int) -> Order:
        order = self.uow.orders.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order
