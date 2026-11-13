from ..exceptions.order import OrderAlreadyCompletedError, OrderNotFoundError
from ..ports import UnitOfWorkProtocol
from ..schemas import OrderStatus


class DeleteOrderUseCase:
    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(self, order_id: int) -> None:
        with self.uow:
            order = self.uow.orders.get_by_id(order_id)
            if order is None:
                raise OrderNotFoundError(order_id)
            if order.status == OrderStatus.completed:
                raise OrderAlreadyCompletedError(order_id)
            if self.uow.orders.delete(order_id) is None:
                raise OrderNotFoundError(order_id)
