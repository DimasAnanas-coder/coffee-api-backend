from sqlalchemy.orm import Session


class BaseRepository:
    """Общая работа репозиториев с сессией и транзакцией."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
