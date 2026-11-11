from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, Query

from .config import Settings, get_settings
from .infrastructure.repository.order import OrderRepository
from .ports import OrderRepositoryProtocol
from .service import OrderService


@lru_cache
def get_repository() -> OrderRepositoryProtocol:
    return OrderRepository()


RepositoryDep = Annotated[OrderRepositoryProtocol, Depends(get_repository)]


def get_service(repository: RepositoryDep) -> OrderService:
    return OrderService(repository)


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


ServiceDep = Annotated[OrderService, Depends(get_service)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
PaginationDep = Annotated[dict[str, int | None], Depends(pagination_params)]
