from ..exceptions.user import UserNotFoundError
from ..ports import UnitOfWorkProtocol


class DeleteUserUseCase:
    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(self, user_id: int) -> None:
        with self.uow:
            if self.uow.users.get_by_id(user_id) is None:
                raise UserNotFoundError(user_id=user_id)
            if self.uow.users.delete(user_id) is None:
                raise UserNotFoundError(user_id=user_id)
