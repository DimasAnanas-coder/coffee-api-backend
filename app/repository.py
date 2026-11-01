from typing import Protocol

from .schemas import Order


class OrderRepositoryProtocol(Protocol):
    """Описывает операции хранилища, нужные сервисному слою."""

    def get_all(self) -> list[Order]: ...

    def get_by_id(self, order_id: int) -> Order | None: ...

    def add(self, order: Order) -> Order: ...

    def update(self, order_id: int, update_data: dict) -> Order | None: ...

    def delete(self, order_id: int) -> Order | None: ...


class OrderRepository:
    def __init__(self) -> None:
        self._orders: list[Order] = []

    def get_all(self) -> list[Order]:
        return list(self._orders) # чтобы вернуть копию списка, а не ссылку на него

    def get_by_id(self, order_id: int) -> Order | None:
        for order in self._orders:
            if order.id == order_id:
                return order
        return None

    def add(self, order: Order) -> Order:
        self._orders.append(order)
        return order

    def update(self, order_id: int, update_data: dict) -> Order | None:
        for index, order in enumerate(self._orders):
            if order.id == order_id:
                updated_order = Order.model_validate({**order.model_dump(), **update_data})
                self._orders[index] = updated_order
                return updated_order
        return None

    def delete(self, order_id: int) -> Order | None:
        for index, order in enumerate(self._orders):
            if order.id == order_id:
                return self._orders.pop(index)
        return None
