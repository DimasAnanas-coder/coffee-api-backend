from sqlalchemy import select

from ...infrastructure.models import Order as OrderModel
from ...schemas import Order, OrderCreate, OrderStatus
from .base import BaseRepository


class OrderRepository(BaseRepository):
    def get_all(
        self,
        order_status: OrderStatus | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Order]:
        statement = select(OrderModel).order_by(OrderModel.id)
        if order_status is not None:
            statement = statement.where(OrderModel.status == order_status.value)
        if limit is not None:
            statement = statement.limit(limit)
        statement = statement.offset(offset)
        records = self.db.scalars(statement).all()
        return [Order.model_validate(record) for record in records]

    def get_by_id(self, order_id: int) -> Order | None:
        record = self.db.get(OrderModel, order_id)
        return Order.model_validate(record) if record is not None else None

    def add(self, order_data: OrderCreate) -> Order:
        record = OrderModel(**order_data.model_dump())
        self.db.add(record)
        self.db.flush()
        self.db.refresh(record)
        return Order.model_validate(record)

    def update(self, order_id: int, update_data: dict) -> Order | None:
        record = self.db.get(OrderModel, order_id)
        if record is None:
            return None
        for field, value in update_data.items():
            setattr(record, field, value.value if isinstance(value, OrderStatus) else value)
        self.db.flush()
        self.db.refresh(record)
        return Order.model_validate(record)

    def delete(self, order_id: int) -> Order | None:
        record = self.db.get(OrderModel, order_id)
        if record is None:
            return None
        result = Order.model_validate(record)
        self.db.delete(record)
        self.db.flush()
        return result
