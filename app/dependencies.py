from typing import Annotated

from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .config import Settings, get_settings
from .infrastructure.database import get_db
from .infrastructure.repository.order import OrderRepository
from .ports import OrderRepositoryProtocol
from .use_cases import (
    CreateOrderUseCase,
    CreateUserUseCase,
    DeleteOrderUseCase,
    DeleteUserUseCase,
    GetOrderUseCase,
    GetUserUseCase,
    ListOrdersUseCase,
    ListUsersUseCase,
    UpdateOrderUseCase,
    UpdateUserUseCase,
)


DbSession = Annotated[Session, Depends(get_db)]


def get_order_repository(db: DbSession) -> OrderRepositoryProtocol:
    return OrderRepository(db)


OrderRepositoryDep = Annotated[OrderRepositoryProtocol, Depends(get_order_repository)]


def get_create_order_use_case(db: DbSession) -> CreateOrderUseCase:
    return CreateOrderUseCase(db)


def get_list_orders_use_case(db: DbSession) -> ListOrdersUseCase:
    return ListOrdersUseCase(db)


def get_order_use_case(db: DbSession) -> GetOrderUseCase:
    return GetOrderUseCase(db)


def get_update_order_use_case(db: DbSession) -> UpdateOrderUseCase:
    return UpdateOrderUseCase(db)


def get_delete_order_use_case(db: DbSession) -> DeleteOrderUseCase:
    return DeleteOrderUseCase(db)


def get_create_user_use_case(db: DbSession) -> CreateUserUseCase:
    return CreateUserUseCase(db)


def get_list_users_use_case(db: DbSession) -> ListUsersUseCase:
    return ListUsersUseCase(db)


def get_user_use_case(db: DbSession) -> GetUserUseCase:
    return GetUserUseCase(db)


def get_update_user_use_case(db: DbSession) -> UpdateUserUseCase:
    return UpdateUserUseCase(db)


def get_delete_user_use_case(db: DbSession) -> DeleteUserUseCase:
    return DeleteUserUseCase(db)


def pagination_params(
    config: Annotated[Settings, Depends(get_settings)],
    limit: Annotated[int | None, Query(ge=1, description="Число записей на странице")] = None,
    offset: Annotated[int, Query(ge=0, description="Число пропускаемых записей")] = 0,
) -> dict[str, int | None]:
    if limit is not None and limit > config.max_page_size:
        raise HTTPException(
            status_code=422,
            detail=f"Параметр limit не может быть больше {config.max_page_size}",
        )
    return {"limit": config.default_page_size if limit is None else limit, "offset": offset}


CreateOrderUseCaseDep = Annotated[CreateOrderUseCase, Depends(get_create_order_use_case)]
ListOrdersUseCaseDep = Annotated[ListOrdersUseCase, Depends(get_list_orders_use_case)]
GetOrderUseCaseDep = Annotated[GetOrderUseCase, Depends(get_order_use_case)]
UpdateOrderUseCaseDep = Annotated[UpdateOrderUseCase, Depends(get_update_order_use_case)]
DeleteOrderUseCaseDep = Annotated[DeleteOrderUseCase, Depends(get_delete_order_use_case)]
CreateUserUseCaseDep = Annotated[CreateUserUseCase, Depends(get_create_user_use_case)]
ListUsersUseCaseDep = Annotated[ListUsersUseCase, Depends(get_list_users_use_case)]
GetUserUseCaseDep = Annotated[GetUserUseCase, Depends(get_user_use_case)]
UpdateUserUseCaseDep = Annotated[UpdateUserUseCase, Depends(get_update_user_use_case)]
DeleteUserUseCaseDep = Annotated[DeleteUserUseCase, Depends(get_delete_user_use_case)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
PaginationDep = Annotated[dict[str, int | None], Depends(pagination_params)]
