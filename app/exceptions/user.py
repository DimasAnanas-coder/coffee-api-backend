class UserNotFoundError(Exception):
    def __init__(self, user_id: int | None = None, email: str | None = None) -> None:
        self.user_id = user_id
        self.email = email
        super().__init__(user_id if user_id is not None else email)


class UserAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(email)
