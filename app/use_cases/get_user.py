from ..exceptions.user import UserNotFoundError
from ..ports import UnitOfWorkProtocol
from ..schemas import User


class GetUserUseCase:
    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(self, user_id: int) -> User:
        user = self.uow.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)
        return user

    def execute_by_email(self, email: str) -> User:
        user = self.uow.users.get_by_email(email)
        if user is None:
            raise UserNotFoundError(email=email)
        return user
