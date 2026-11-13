from sqlalchemy.orm import Session

from ..exceptions.user import UserAlreadyExistsError
from ..infrastructure.repository.user import UserRepository
from ..schemas import User, UserCreate


class CreateUserUseCase:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = UserRepository(session)

    def execute(self, user_data: UserCreate) -> User:
        with self.session.begin():
            if self.users.get_by_email(user_data.email) is not None:
                raise UserAlreadyExistsError(user_data.email)
            return self.users.add(user_data)
