from typing import Protocol

from .schemas import Order, OrderCreate, OrderStatus


class OrderRepositoryProtocol(Protocol):
    """Описывает операции хранилища, нужные сервисному слою."""

    def get_all(
        self,
        order_status: OrderStatus | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Order]: ...

    def get_by_id(self, order_id: int) -> Order | None: ...

    def add(self, order_data: OrderCreate) -> Order: ...

    def update(self, order_id: int, update_data: dict) -> Order | None: ...

    def delete(self, order_id: int) -> Order | None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
