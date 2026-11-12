from typing import Annotated

from fastapi import APIRouter, Query, status

from ..dependencies import UserServiceDep
from ..schemas import User, UserCreate

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED, summary="Создать пользователя")
def create_user(user_data: UserCreate, service: UserServiceDep) -> User:
    return service.create_user(user_data)


@router.get("/by-email", response_model=User, summary="Найти пользователя по email")
def get_user_by_email(
    service: UserServiceDep,
    email: Annotated[str, Query(min_length=1)],
) -> User:
    return service.get_user_by_email(email)


@router.get("/{user_id}", response_model=User, summary="Получить пользователя по ID")
def get_user(user_id: int, service: UserServiceDep) -> User:
    return service.get_user(user_id)
