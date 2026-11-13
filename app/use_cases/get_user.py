from sqlalchemy.orm import Session

from ..exceptions.user import UserNotFoundError
from ..infrastructure.repository.user import UserRepository
from ..schemas import User


class GetUserUseCase:
    def __init__(self, session: Session) -> None:
        self.users = UserRepository(session)

    def execute(self, user_id: int) -> User:
        user = self.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)
        return user

    def execute_by_email(self, email: str) -> User:
        user = self.users.get_by_email(email)
        if user is None:
            raise UserNotFoundError(email=email)
        return user
