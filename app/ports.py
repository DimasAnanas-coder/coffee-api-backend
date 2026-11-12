from typing import Protocol

from .schemas import Order, OrderCreate, OrderStatus, User, UserCreate


class BaseRepositoryProtocol(Protocol):
    """Операции транзакции, общие для всех репозиториев."""

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


class OrderRepositoryProtocol(BaseRepositoryProtocol, Protocol):
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


class UserRepositoryProtocol(BaseRepositoryProtocol, Protocol):
    """Описывает операции хранилища пользователей."""

    def get_by_id(self, user_id: int) -> User | None: ...

    def get_by_email(self, email: str) -> User | None: ...

    def add(self, user_data: UserCreate) -> User: ...
