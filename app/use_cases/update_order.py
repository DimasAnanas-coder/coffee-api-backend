from sqlalchemy.orm import Session

from ..exceptions.order import OrderAlreadyCompletedError, OrderNotFoundError
from ..infrastructure.repository.order import OrderRepository
from ..schemas import Order, OrderStatus, OrderUpdate


class UpdateOrderUseCase:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.orders = OrderRepository(session)

    def execute(self, order_id: int, order_data: OrderUpdate) -> Order:
        with self.session.begin():
            order = self.orders.get_by_id(order_id)
            if order is None:
                raise OrderNotFoundError(order_id)
            if order.status == OrderStatus.completed:
                raise OrderAlreadyCompletedError(order_id)

            updated_order = self.orders.update(order_id, order_data.model_dump(exclude_unset=True))
            if updated_order is None:
                raise OrderNotFoundError(order_id)
            return updated_order
