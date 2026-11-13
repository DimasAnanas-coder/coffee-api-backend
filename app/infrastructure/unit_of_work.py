from types import TracebackType

from sqlalchemy.orm import Session

from .repository.order import OrderRepository
from .repository.user import UserRepository


class SqlAlchemyUnitOfWork:
    """SQLAlchemy реализация Unit of Work для одной сессии."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.orders = OrderRepository(session)
        self.users = UserRepository(session)
        self._transaction = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self._transaction = self.session.begin()
        self._transaction.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._transaction is None:
            raise RuntimeError("Unit of Work transaction was not started")
        try:
            self._transaction.__exit__(exc_type, exc_value, traceback)
        finally:
            self._transaction = None
