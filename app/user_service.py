from .ports import UserRepositoryProtocol
from .schemas import User, UserCreate
from .user_exceptions import UserAlreadyExistsError, UserNotFoundError


class UserService:
    def __init__(self, repository: UserRepositoryProtocol) -> None:
        self.repository = repository

    def create_user(self, user_data: UserCreate) -> User:
        try:
            if self.repository.get_by_email(user_data.email) is not None:
                raise UserAlreadyExistsError(user_data.email)
            user = self.repository.add(user_data)
            self.repository.commit()
            return user
        except Exception:
            self.repository.rollback()
            raise

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_by_email(email)
        if user is None:
            raise UserNotFoundError(email=email)
        return user
