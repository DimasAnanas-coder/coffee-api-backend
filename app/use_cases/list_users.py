from sqlalchemy.orm import Session

from ..infrastructure.repository.user import UserRepository
from ..schemas import User


class ListUsersUseCase:
    def __init__(self, session: Session) -> None:
        self.users = UserRepository(session)

    def execute(self, limit: int | None = None, offset: int = 0) -> list[User]:
        return self.users.get_all(limit=limit, offset=offset)
