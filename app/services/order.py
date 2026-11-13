from sqlalchemy.orm import Session

from ..exceptions.order import OrderAlreadyCompletedError, OrderNotFoundError
from ..ports import OrderRepositoryProtocol
from ..schemas import Order, OrderCreate, OrderStatus, OrderUpdate


class OrderService:
    def __init__(self, repository: OrderRepositoryProtocol, session: Session) -> None:
        self.repository = repository
        self.session = session

    def create_order(self, order_data: OrderCreate) -> Order:
        with self.session.begin():
            return self.repository.add(order_data)

    def list_orders(
        self,
        order_status: OrderStatus | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Order]:
        return self.repository.get_all(
            order_status=order_status,
            limit=limit,
            offset=offset,
        )

    def get_order(self, order_id: int) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def update_order(self, order_id: int, order_data: OrderUpdate) -> Order:
        with self.session.begin():
            order = self.get_order(order_id)
            self._ensure_not_completed(order)
            updated_order = self.repository.update(order_id, order_data.model_dump(exclude_unset=True))
            if updated_order is None:
                raise OrderNotFoundError(order_id)
            return updated_order

    def delete_order(self, order_id: int) -> None:
        with self.session.begin():
            order = self.get_order(order_id)
            self._ensure_not_completed(order)
            if self.repository.delete(order_id) is None:
                raise OrderNotFoundError(order_id)

    @staticmethod
    def _ensure_not_completed(order: Order) -> None:
        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order.id)
