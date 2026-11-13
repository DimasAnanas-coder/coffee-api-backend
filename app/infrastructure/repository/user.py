from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ...exceptions.user import UserHasOrdersError
from ...infrastructure.models import User as UserModel
from ...schemas import User, UserCreate
from .base import BaseRepository


class UserRepository(BaseRepository):
    def get_all(self, limit: int | None = None, offset: int = 0) -> list[User]:
        statement = select(UserModel).order_by(UserModel.id).offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        return [User.model_validate(record) for record in self.db.scalars(statement).all()]

    def get_by_id(self, user_id: int) -> User | None:
        record = self.db.get(UserModel, user_id)
        return User.model_validate(record) if record is not None else None

    def get_by_id_for_update(self, user_id: int) -> User | None:
        statement = select(UserModel).where(UserModel.id == user_id).with_for_update()
        record = self.db.scalar(statement)
        return User.model_validate(record) if record is not None else None

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        record = self.db.scalar(statement)
        return User.model_validate(record) if record is not None else None

    def set_balance(self, user_id: int, balance: Decimal) -> None:
        record = self.db.get(UserModel, user_id)
        if record is None:
            return
        record.balance = balance
        self.db.flush()

    def add(self, user_data: UserCreate) -> User:
        record = UserModel(**user_data.model_dump())
        self.db.add(record)
        self.db.flush()
        self.db.refresh(record)
        return User.model_validate(record)

    def update(self, user_id: int, update_data: dict) -> User | None:
        record = self.db.get(UserModel, user_id)
        if record is None:
            return None
        for field, value in update_data.items():
            setattr(record, field, value)
        self.db.flush()
        self.db.refresh(record)
        return User.model_validate(record)

    def delete(self, user_id: int) -> User | None:
        record = self.db.get(UserModel, user_id)
        if record is None:
            return None
        user = User.model_validate(record)
        self.db.delete(record)
        try:
            self.db.flush()
        except IntegrityError as exc:
            raise UserHasOrdersError(user_id) from exc
        return user
