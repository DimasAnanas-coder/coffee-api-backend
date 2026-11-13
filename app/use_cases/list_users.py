from ..ports import UnitOfWorkProtocol
from ..schemas import User


class ListUsersUseCase:
    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(self, limit: int | None = None, offset: int = 0) -> list[User]:
        return self.uow.users.get_all(limit=limit, offset=offset)
