from typing import Protocol

from .schemas import Order


class OrderRepositoryProtocol(Protocol):
    """Описывает операции хранилища, нужные сервисному слою."""

    def get_all(self) -> list[Order]: ...

    def get_by_id(self, order_id: int) -> Order | None: ...

    def add(self, order: Order) -> Order: ...

    def update(self, order_id: int, update_data: dict) -> Order | None: ...

    def delete(self, order_id: int) -> Order | None: ...
