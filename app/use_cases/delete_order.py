from sqlalchemy.orm import Session

from ..exceptions.order import OrderAlreadyCompletedError, OrderNotFoundError
from ..infrastructure.repository.order import OrderRepository
from ..schemas import OrderStatus


class DeleteOrderUseCase:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.orders = OrderRepository(session)

    def execute(self, order_id: int) -> None:
        with self.session.begin():
            order = self.orders.get_by_id(order_id)
            if order is None:
                raise OrderNotFoundError(order_id)
            if order.status == OrderStatus.completed:
                raise OrderAlreadyCompletedError(order_id)
            if self.orders.delete(order_id) is None:
                raise OrderNotFoundError(order_id)
