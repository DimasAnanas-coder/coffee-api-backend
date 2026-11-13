from ..exceptions.user import UserAlreadyExistsError
from ..ports import UnitOfWorkProtocol
from ..schemas import User, UserCreate


class CreateUserUseCase:
    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(self, user_data: UserCreate) -> User:
        with self.uow:
            if self.uow.users.get_by_email(user_data.email) is not None:
                raise UserAlreadyExistsError(user_data.email)
            return self.uow.users.add(user_data)
