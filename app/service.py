from datetime import datetime

from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .ports import OrderRepositoryProtocol
from .schemas import Order, OrderCreate, OrderStatus, OrderUpdate


class OrderService:
    def __init__(self, repository: OrderRepositoryProtocol) -> None:
        self.repository = repository

    def create_order(self, order_data: OrderCreate) -> Order:
        orders = self.repository.get_all()
        order = Order(
            id=max((item.id for item in orders), default=0) + 1,
            **order_data.model_dump(),
            status=OrderStatus.pending,
            created_at=datetime.now().astimezone(),
        )
        return self.repository.add(order)

    def list_orders(
        self,
        order_status: OrderStatus | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Order]:
        result = self.repository.get_all()
        if order_status is not None:
            result = [order for order in result if order.status == order_status]
        page_size = limit if limit is not None else len(result)
        return result[offset : offset + page_size]

    def get_order(self, order_id: int) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def update_order(self, order_id: int, order_data: OrderUpdate) -> Order:
        order = self.get_order(order_id)
        self._ensure_not_completed(order)
        updated_order = self.repository.update(order_id, order_data.model_dump(exclude_unset=True))
        if updated_order is None:
            raise OrderNotFoundError(order_id)
        return updated_order

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        self._ensure_not_completed(order)
        if self.repository.delete(order_id) is None:
            raise OrderNotFoundError(order_id)

    @staticmethod
    def _ensure_not_completed(order: Order) -> None:
        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order.id)
