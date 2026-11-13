from sqlalchemy.orm import Session

from ..exceptions.user import UserAlreadyExistsError, UserNotFoundError
from ..ports import UserRepositoryProtocol
from ..schemas import User, UserCreate


class UserService:
    def __init__(self, repository: UserRepositoryProtocol, session: Session) -> None:
        self.repository = repository
        self.session = session

    def create_user(self, user_data: UserCreate) -> User:
        with self.session.begin():
            if self.repository.get_by_email(user_data.email) is not None:
                raise UserAlreadyExistsError(user_data.email)
            return self.repository.add(user_data)

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
