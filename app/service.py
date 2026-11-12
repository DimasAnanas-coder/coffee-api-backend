from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .ports import OrderRepositoryProtocol
from .schemas import Order, OrderCreate, OrderStatus, OrderUpdate


class OrderService:
    def __init__(self, repository: OrderRepositoryProtocol) -> None:
        self.repository = repository

    def create_order(self, order_data: OrderCreate) -> Order:
        try:
            order = self.repository.add(order_data)
            self.repository.commit()
            return order
        except Exception:
            self.repository.rollback()
            raise

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
        try:
            order = self.get_order(order_id)
            self._ensure_not_completed(order)
            updated_order = self.repository.update(order_id, order_data.model_dump(exclude_unset=True))
            if updated_order is None:
                raise OrderNotFoundError(order_id)
            self.repository.commit()
            return updated_order
        except Exception:
            self.repository.rollback()
            raise

    def delete_order(self, order_id: int) -> None:
        try:
            order = self.get_order(order_id)
            self._ensure_not_completed(order)
            if self.repository.delete(order_id) is None:
                raise OrderNotFoundError(order_id)
            self.repository.commit()
        except Exception:
            self.repository.rollback()
            raise

    @staticmethod
    def _ensure_not_completed(order: Order) -> None:
        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order.id)
