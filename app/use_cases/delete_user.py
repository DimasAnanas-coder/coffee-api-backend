from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..exceptions.user import UserHasOrdersError, UserNotFoundError
from ..infrastructure.repository.user import UserRepository


class DeleteUserUseCase:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = UserRepository(session)

    def execute(self, user_id: int) -> None:
        try:
            with self.session.begin():
                if self.users.get_by_id(user_id) is None:
                    raise UserNotFoundError(user_id=user_id)
                if self.users.delete(user_id) is None:
                    raise UserNotFoundError(user_id=user_id)
        except IntegrityError as exc:
            raise UserHasOrdersError(user_id) from exc
