from typing import Annotated

from fastapi import APIRouter, Query, Request, Response, status
from fastapi.responses import JSONResponse

from ..dependencies import (
    CreateUserUseCaseDep,
    DeleteUserUseCaseDep,
    GetUserUseCaseDep,
    ListUsersUseCaseDep,
    PaginationDep,
    UpdateUserUseCaseDep,
)
from ..exceptions.user import UserAlreadyExistsError, UserHasOrdersError, UserNotFoundError
from ..schemas import User, UserCreate, UserUpdate

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


async def user_has_orders_handler(request: Request, exc: UserHasOrdersError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"Нельзя удалить пользователя {exc.user_id}: у него есть заказы"},
    )


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED, summary="Создать пользователя")
def create_user(user_data: UserCreate, use_case: CreateUserUseCaseDep) -> User:
    return use_case.execute(user_data)


@router.get("", response_model=list[User], summary="Получить список пользователей")
def list_users(use_case: ListUsersUseCaseDep, pagination: PaginationDep) -> list[User]:
    return use_case.execute(**pagination)


@router.get("/by-email", response_model=User, summary="Найти пользователя по email")
def get_user_by_email(
    use_case: GetUserUseCaseDep,
    email: Annotated[str, Query(min_length=1)],
) -> User:
    return use_case.execute_by_email(email)


@router.get("/{user_id}", response_model=User, summary="Получить пользователя по ID")
def get_user(user_id: int, use_case: GetUserUseCaseDep) -> User:
    return use_case.execute(user_id)


@router.patch("/{user_id}", response_model=User, summary="Обновить пользователя")
def update_user(user_id: int, user_data: UserUpdate, use_case: UpdateUserUseCaseDep) -> User:
    return use_case.execute(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Удалить пользователя",
)
def delete_user(user_id: int, use_case: DeleteUserUseCaseDep) -> Response:
    use_case.execute(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
