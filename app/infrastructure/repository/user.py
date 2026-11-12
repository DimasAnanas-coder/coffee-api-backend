from sqlalchemy import select

from ...infrastructure.models import User as UserModel
from ...schemas import User, UserCreate
from .base import BaseRepository


class UserRepository(BaseRepository):
    def get_by_id(self, user_id: int) -> User | None:
        record = self.db.get(UserModel, user_id)
        return User.model_validate(record) if record is not None else None

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        record = self.db.scalar(statement)
        return User.model_validate(record) if record is not None else None

    def add(self, user_data: UserCreate) -> User:
        record = UserModel(**user_data.model_dump())
        self.db.add(record)
        self.db.flush()
        self.db.refresh(record)
        return User.model_validate(record)
