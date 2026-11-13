from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0, description="Идентификатор пользователя", examples=[1])
    email: str = Field(min_length=1, description="Email пользователя", examples=["irina@example.com"])
    balance: Decimal = Field(ge=0, description="Баланс пользователя", examples=["500.00"])


class UserCreate(BaseModel):
    email: str = Field(min_length=1, description="Email пользователя", examples=["irina@example.com"])
    balance: Decimal = Field(ge=0, description="Начальный баланс", examples=["500.00"])


class UserUpdate(BaseModel):
    email: str | None = Field(default=None, min_length=1, description="Email пользователя")
    balance: Decimal | None = Field(default=None, ge=0, description="Баланс пользователя")


class OrderCreate(BaseModel):
    user_id: int = Field(gt=0, description="Идентификатор пользователя", examples=[1])
    amount: Decimal = Field(gt=0, description="Сумма заказа", examples=["120.00"])


class OrderUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, description="Новая сумма заказа", examples=["120.00"])
    status: OrderStatus | None = Field(default=None, description="Новый статус заказа", examples=["ready"])


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Идентификатор заказа", examples=[1])
    user_id: int = Field(gt=0, description="Идентификатор пользователя", examples=[1])
    amount: Decimal = Field(gt=0, description="Сумма заказа", examples=["120.00"])
    status: OrderStatus = Field(description="Статус заказа", examples=["pending"])
