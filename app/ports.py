from decimal import Decimal
from types import TracebackType
from typing import Protocol

from .schemas import Order, OrderCreate, OrderStatus, User, UserCreate


class OrderRepositoryProtocol(Protocol):
    """Описывает операции хранилища, нужные прикладному слою."""

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


class UserRepositoryProtocol(Protocol):
    """Описывает операции хранилища пользователей."""

    def get_all(self, limit: int | None = None, offset: int = 0) -> list[User]: ...

    def get_by_id(self, user_id: int) -> User | None: ...

    def get_by_id_for_update(self, user_id: int) -> User | None: ...

    def get_by_email(self, email: str) -> User | None: ...

    def add(self, user_data: UserCreate) -> User: ...

    def update(self, user_id: int, update_data: dict) -> User | None: ...

    def delete(self, user_id: int) -> User | None: ...

    def set_balance(self, user_id: int, balance: Decimal) -> None: ...


class UnitOfWorkProtocol(Protocol):
    """Даёт use case репозитории и управляет общей транзакцией."""

    orders: OrderRepositoryProtocol
    users: UserRepositoryProtocol

    def __enter__(self) -> "UnitOfWorkProtocol": ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
