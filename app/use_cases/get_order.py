from sqlalchemy.orm import Session

from ..exceptions.order import OrderNotFoundError
from ..infrastructure.repository.order import OrderRepository
from ..schemas import Order


class GetOrderUseCase:
    def __init__(self, session: Session) -> None:
        self.orders = OrderRepository(session)

    def execute(self, order_id: int) -> Order:
        order = self.orders.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order
