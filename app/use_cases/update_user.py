from sqlalchemy.orm import Session

from ..exceptions.user import UserAlreadyExistsError, UserNotFoundError
from ..infrastructure.repository.user import UserRepository
from ..schemas import User, UserUpdate


class UpdateUserUseCase:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = UserRepository(session)

    def execute(self, user_id: int, user_data: UserUpdate) -> User:
        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
        with self.session.begin():
            user = self.users.get_by_id(user_id)
            if user is None:
                raise UserNotFoundError(user_id=user_id)
            email = update_data.get("email")
            if email is not None:
                existing_user = self.users.get_by_email(email)
                if existing_user is not None and existing_user.id != user_id:
                    raise UserAlreadyExistsError(email)
            updated_user = self.users.update(user_id, update_data)
            if updated_user is None:
                raise UserNotFoundError(user_id=user_id)
            return updated_user
