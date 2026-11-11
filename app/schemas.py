from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class DrinkSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0, description="Идентификатор пользователя", examples=[1])
    email: str = Field(min_length=1, description="Email пользователя", examples=["irina@example.com"])
    balance: Decimal = Field(ge=0, description="Баланс пользователя", examples=["500.00"])


class OrderCreate(BaseModel):
    user_id: int = Field(gt=0, description="Идентификатор пользователя", examples=[1])
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
    user_id: int = Field(gt=0, description="Идентификатор пользователя", examples=[1])
    drink: str = Field(description="Название напитка", examples=["Латте"])
    size: DrinkSize = Field(description="Размер напитка", examples=["medium"])
    quantity: int = Field(gt=0, description="Количество напитков", examples=[2])
    customer_name: str | None = Field(description="Имя клиента", examples=["Ирина"])
    status: OrderStatus = Field(description="Статус заказа", examples=["pending"])
    created_at: datetime = Field(description="Время создания заказа")
