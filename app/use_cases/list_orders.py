from sqlalchemy.orm import Session

from ..infrastructure.repository.order import OrderRepository
from ..schemas import Order, OrderStatus


class ListOrdersUseCase:
    def __init__(self, session: Session) -> None:
        self.orders = OrderRepository(session)

    def execute(
        self,
        order_status: OrderStatus | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Order]:
        return self.orders.get_all(order_status=order_status, limit=limit, offset=offset)
