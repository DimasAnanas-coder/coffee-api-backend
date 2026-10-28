from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Учёт заказов кофейни"
    default_page_size: int = Field(default=10, ge=1)
    max_page_size: int = Field(default=50, ge=1)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


class DrinkSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"


class OrderCreate(BaseModel):
    drink: str = Field(min_length=1, description="Название напитка из меню", examples=["Латте"])
    size: DrinkSize = Field(description="Размер напитка", examples=["medium"])
    quantity: int = Field(gt=0, description="Количество напитков", examples=[2])
    customer_name: str | None = Field(default=None, min_length=1, description="Имя клиента", examples=["Ирина"])


class OrderUpdate(BaseModel):
    drink: str | None = Field(default=None, min_length=1, description="Новое название напитка", examples=["Капучино"])
    size: DrinkSize | None = Field(default=None, description="Новый размер напитка", examples=["large"])
    quantity: int | None = Field(default=None, gt=0, description="Новое количество", examples=[1])
    customer_name: str | None = Field(default=None, min_length=1, description="Новое имя клиента", examples=["Ирина"])
    status: OrderStatus | None = Field(default=None, description="Новый статус заказа", examples=["ready"])


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Идентификатор заказа", examples=[1])
    drink: str = Field(description="Название напитка", examples=["Латте"])
    size: DrinkSize = Field(description="Размер напитка", examples=["medium"])
    quantity: int = Field(gt=0, description="Количество напитков", examples=[2])
    customer_name: str | None = Field(description="Имя клиента", examples=["Ирина"])
    status: OrderStatus = Field(description="Статус заказа", examples=["pending"])
    created_at: datetime = Field(description="Время создания заказа")


def get_settings() -> Settings:
    return settings


SettingsDependency = Annotated[Settings, Depends(get_settings)]

app = FastAPI(
    title=settings.app_name,
    description="Сервис учёта заказов кофейни. Данные хранятся в памяти процесса.",
    version="1.0.0",
)

orders: dict[int, Order] = {}
next_order_id = 1


@app.get("/", tags=["Сервис"], summary="Проверить работу сервиса")
def root() -> dict[str, str]:
    """Возвращает приветственное сообщение."""
    return {"message": f"Добро пожаловать в сервис «{settings.app_name}»!"}


@app.get("/info", tags=["Сервис"], summary="Получить информацию о сервисе")
def info(config: SettingsDependency) -> dict[str, str | int]:
    """Возвращает название сервиса и число заказов в памяти."""
    return {"name": config.app_name, "orders_count": len(orders)}


@app.post(
    "/orders",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    tags=["Заказы"],
    summary="Создать заказ",
)
def create_order(order_data: OrderCreate) -> Order:
    """Создаёт заказ со статусом pending и временем создания."""
    global next_order_id
    order = Order(
        id=next_order_id,
        **order_data.model_dump(),
        status=OrderStatus.pending,
        created_at=datetime.now().astimezone(),
    )
    orders[order.id] = order
    next_order_id += 1
    return order


@app.get(
    "/orders",
    response_model=list[Order],
    tags=["Заказы"],
    summary="Получить список заказов",
)
def list_orders(
    config: SettingsDependency,
    order_status: Annotated[OrderStatus | None, Query(alias="status", description="Фильтр по статусу")] = None,
    limit: Annotated[int | None, Query(ge=1, description="Число заказов на странице")] = None,
    offset: Annotated[int, Query(ge=0, description="Число пропускаемых заказов")] = 0,
) -> list[Order]:
    """Возвращает заказы с необязательными фильтром и постраничной выдачей."""
    page_size = config.default_page_size if limit is None else limit
    if page_size > config.max_page_size:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Параметр limit не может быть больше {config.max_page_size}",
        )
    result = list(orders.values())
    if order_status is not None:
        result = [order for order in result if order.status == order_status]
    return result[offset : offset + page_size]


@app.get(
    "/orders/{order_id}",
    response_model=Order,
    tags=["Заказы"],
    summary="Получить заказ по ID",
)
def get_order(order_id: int) -> Order:
    """Возвращает один заказ или ошибку 404, если его нет."""
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    return order


@app.patch(
    "/orders/{order_id}",
    response_model=Order,
    tags=["Заказы"],
    summary="Частично обновить заказ",
)
def update_order(order_id: int, order_data: OrderUpdate) -> Order:
    """Обновляет только переданные поля; время создания не меняется."""
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    updated_data = order.model_dump()
    updated_data.update(order_data.model_dump(exclude_unset=True))
    updated_order = Order.model_validate(updated_data)
    orders[order_id] = updated_order
    return updated_order


@app.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    tags=["Заказы"],
    summary="Отменить заказ",
)
def delete_order(order_id: int) -> Response:
    """Удаляет заказ и возвращает ответ без тела."""
    if order_id not in orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    del orders[order_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
