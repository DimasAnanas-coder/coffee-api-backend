from ..exceptions.order import OrderAlreadyCompletedError, OrderNotFoundError
from ..ports import UnitOfWorkProtocol
from ..schemas import Order, OrderStatus, OrderUpdate


class UpdateOrderUseCase:
    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(self, order_id: int, order_data: OrderUpdate) -> Order:
        with self.uow:
            order = self.uow.orders.get_by_id(order_id)
            if order is None:
                raise OrderNotFoundError(order_id)
            if order.status == OrderStatus.completed:
                raise OrderAlreadyCompletedError(order_id)

            updated_order = self.uow.orders.update(order_id, order_data.model_dump(exclude_unset=True))
            if updated_order is None:
                raise OrderNotFoundError(order_id)
            return updated_order
