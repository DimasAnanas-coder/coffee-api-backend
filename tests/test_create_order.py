from decimal import Decimal

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker

from app.exceptions.order import InsufficientBalanceError
from app.exceptions.user import UserNotFoundError
from app.infrastructure.models import Base, Order as OrderModel, User as UserModel
from app.infrastructure.repository.order import OrderRepository
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.schemas import OrderCreate, OrderStatus
from app.use_cases.create_order import CreateOrderUseCase


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
    with factory.begin() as session:
        session.add(UserModel(email="buyer@example.com", balance=Decimal("100.00")))
    yield factory
    engine.dispose()


def test_create_order_debits_balance_and_saves_pending_order(session_factory):
    with session_factory() as session:
        order = CreateOrderUseCase(SqlAlchemyUnitOfWork(session)).execute(
            OrderCreate(user_id=1, amount=Decimal("25.00"))
        )

    assert order.status == OrderStatus.pending
    with session_factory() as verification_session:
        balance = verification_session.scalar(select(UserModel.balance).where(UserModel.id == 1))
        order_count = verification_session.scalar(select(func.count()).select_from(OrderModel))

    assert balance == Decimal("75.00")
    assert order_count == 1


def test_create_order_rejects_non_positive_amount(session_factory):
    order_data = OrderCreate.model_construct(user_id=1, amount=Decimal("0.00"))
    with session_factory() as session:
        use_case = CreateOrderUseCase(SqlAlchemyUnitOfWork(session))

        with pytest.raises(ValueError, match="положительной"):
            use_case.execute(order_data)


def test_create_order_rejects_missing_user(session_factory):
    with session_factory() as session:
        use_case = CreateOrderUseCase(SqlAlchemyUnitOfWork(session))

        with pytest.raises(UserNotFoundError):
            use_case.execute(OrderCreate(user_id=999, amount=Decimal("10.00")))


def test_create_order_rejects_insufficient_balance(session_factory):
    with session_factory() as session:
        use_case = CreateOrderUseCase(SqlAlchemyUnitOfWork(session))

        with pytest.raises(InsufficientBalanceError):
            use_case.execute(OrderCreate(user_id=1, amount=Decimal("100.01")))

    with session_factory() as verification_session:
        balance = verification_session.scalar(select(UserModel.balance).where(UserModel.id == 1))
        order_count = verification_session.scalar(select(func.count()).select_from(OrderModel))

    assert balance == Decimal("100.00")
    assert order_count == 0


class FailingOrderRepository(OrderRepository):
    def add(self, order_data: OrderCreate):
        raise RuntimeError("intentional failure before order insert")


def test_failure_after_debit_rolls_back_balance_and_order(session_factory):
    with session_factory() as session:
        uow = SqlAlchemyUnitOfWork(session)
        uow.orders = FailingOrderRepository(session)
        use_case = CreateOrderUseCase(uow)

        with pytest.raises(RuntimeError, match="intentional failure"):
            use_case.execute(OrderCreate(user_id=1, amount=Decimal("25.00")))

    # Check durable state through a new session after the injected failure.
    with session_factory() as verification_session:
        balance = verification_session.scalar(select(UserModel.balance).where(UserModel.id == 1))
        order_count = verification_session.scalar(select(func.count()).select_from(OrderModel))

    assert balance == Decimal("100.00")
    assert order_count == 0
