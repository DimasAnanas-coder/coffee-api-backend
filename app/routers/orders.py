from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from ..dependencies import PaginationDep, ServiceDep
from ..schemas import Order, OrderCreate, OrderStatus, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED, summary="Создать заказ")
def create_order(order_data: OrderCreate, service: ServiceDep) -> Order:
    """Создаёт заказ со статусом pending и временем создания."""
    return service.create_order(order_data)


@router.get("", response_model=list[Order], summary="Получить список заказов")
def list_orders(
    service: ServiceDep,
    pagination: PaginationDep,
    order_status: Annotated[OrderStatus | None, Query(alias="status", description="Фильтр по статусу")] = None,
) -> list[Order]:
    """Возвращает заказы с необязательными фильтром и постраничной выдачей."""
    return service.list_orders(order_status=order_status, **pagination)


@router.get("/{order_id}", response_model=Order, summary="Получить заказ по ID")
def get_order(order_id: int, service: ServiceDep) -> Order:
    """Возвращает один заказ по идентификатору."""
    return service.get_order(order_id)


@router.patch("/{order_id}", response_model=Order, summary="Частично обновить заказ")
def update_order(order_id: int, order_data: OrderUpdate, service: ServiceDep) -> Order:
    """Обновляет только переданные поля заказа."""
    return service.update_order(order_id, order_data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, summary="Отменить заказ")
def delete_order(order_id: int, service: ServiceDep) -> Response:
    """Удаляет заказ и возвращает ответ без тела."""
    service.delete_order(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
