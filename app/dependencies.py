from typing import Annotated

from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .config import Settings, get_settings
from .infrastructure.database import get_db
from .infrastructure.repository.order import OrderRepository
from .ports import OrderRepositoryProtocol
from .infrastructure.repository.user import UserRepository
from .ports import UserRepositoryProtocol
from .services import UserService
from .use_cases import (
    CreateOrderUseCase,
    DeleteOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
    UpdateOrderUseCase,
)


DbSession = Annotated[Session, Depends(get_db)]


def get_order_repository(db: DbSession) -> OrderRepositoryProtocol:
    return OrderRepository(db)


OrderRepositoryDep = Annotated[OrderRepositoryProtocol, Depends(get_order_repository)]


def get_user_repository(db: DbSession) -> UserRepositoryProtocol:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepositoryProtocol, Depends(get_user_repository)]


def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository, repository.db)


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


def pagination_params(
    config: Annotated[Settings, Depends(get_settings)],
    limit: Annotated[int | None, Query(ge=1, description="Число заказов на странице")] = None,
    offset: Annotated[int, Query(ge=0, description="Число пропускаемых заказов")] = 0,
) -> dict[str, int | None]:
    if limit is not None and limit > config.max_page_size:
        raise HTTPException(
            status_code=422,
            detail=f"Параметр limit не может быть больше {config.max_page_size}",
        )
    return {"limit": config.default_page_size if limit is None else limit, "offset": offset}


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
CreateOrderUseCaseDep = Annotated[CreateOrderUseCase, Depends(get_create_order_use_case)]
ListOrdersUseCaseDep = Annotated[ListOrdersUseCase, Depends(get_list_orders_use_case)]
GetOrderUseCaseDep = Annotated[GetOrderUseCase, Depends(get_order_use_case)]
UpdateOrderUseCaseDep = Annotated[UpdateOrderUseCase, Depends(get_update_order_use_case)]
DeleteOrderUseCaseDep = Annotated[DeleteOrderUseCase, Depends(get_delete_order_use_case)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
PaginationDep = Annotated[dict[str, int | None], Depends(pagination_params)]
