from typing import Annotated

from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse

from ..dependencies import UserServiceDep
from ..schemas import User, UserCreate
from ..user_exceptions import UserAlreadyExistsError, UserNotFoundError

router = APIRouter(prefix="/users", tags=["Пользователи"])


async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    detail = (
        f"Пользователь с id={exc.user_id} не найден"
        if exc.user_id is not None
        else f"Пользователь {exc.email} не найден"
    )
    return JSONResponse(status_code=404, content={"detail": detail})


async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"Пользователь с email={exc.email} уже существует"},
    )


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
