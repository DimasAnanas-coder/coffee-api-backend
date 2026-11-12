from typing import Annotated

from fastapi import APIRouter, Query, Request, Response, status
from fastapi.responses import JSONResponse

from ..dependencies import OrderServiceDep, PaginationDep
from ..exceptions.order import OrderAlreadyCompletedError, OrderNotFoundError
from ..schemas import Order, OrderCreate, OrderStatus, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Заказы"])


async def order_not_found_handler(request: Request, exc: OrderNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Заказ с id={exc.order_id} не найден"},
    )


async def order_already_completed_handler(request: Request, exc: OrderAlreadyCompletedError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"Заказ {exc.order_id} уже выполнен и не может быть изменён"},
    )


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED, summary="Создать заказ")
def create_order(order_data: OrderCreate, service: OrderServiceDep) -> Order:
    """Создаёт заказ со статусом pending и временем создания."""
    return service.create_order(order_data)


@router.get("", response_model=list[Order], summary="Получить список заказов")
def list_orders(
    service: OrderServiceDep,
    pagination: PaginationDep,
    order_status: Annotated[OrderStatus | None, Query(alias="status", description="Фильтр по статусу")] = None,
) -> list[Order]:
    """Возвращает заказы с необязательными фильтром и постраничной выдачей."""
    return service.list_orders(order_status=order_status, **pagination)


@router.get("/{order_id}", response_model=Order, summary="Получить заказ по ID")
def get_order(order_id: int, service: OrderServiceDep) -> Order:
    """Возвращает один заказ по идентификатору."""
    return service.get_order(order_id)


@router.patch("/{order_id}", response_model=Order, summary="Частично обновить заказ")
def update_order(order_id: int, order_data: OrderUpdate, service: OrderServiceDep) -> Order:
    """Обновляет только переданные поля заказа."""
    return service.update_order(order_id, order_data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, summary="Отменить заказ")
def delete_order(order_id: int, service: OrderServiceDep) -> Response:
    """Удаляет заказ и возвращает ответ без тела."""
    service.delete_order(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
