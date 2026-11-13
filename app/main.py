from fastapi import FastAPI

from .config import get_settings
from .dependencies import OrderRepositoryDep, SettingsDep
from .exceptions.order import InsufficientBalanceError, OrderAlreadyCompletedError, OrderNotFoundError
from .routers import orders, users
from .exceptions.user import UserAlreadyExistsError, UserNotFoundError

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Сервис учёта пользователей и заказов в PostgreSQL.",
    version="1.0.0",
)
app.include_router(orders.router)
app.include_router(users.router)
app.add_exception_handler(OrderNotFoundError, orders.order_not_found_handler)
app.add_exception_handler(OrderAlreadyCompletedError, orders.order_already_completed_handler)
app.add_exception_handler(InsufficientBalanceError, orders.insufficient_balance_handler)
app.add_exception_handler(UserNotFoundError, users.user_not_found_handler)
app.add_exception_handler(UserAlreadyExistsError, users.user_already_exists_handler)


@app.get("/", tags=["Сервис"], summary="Проверить работу сервиса")
def root() -> dict[str, str]:
    """Возвращает приветственное сообщение."""
    return {"message": f"Добро пожаловать в сервис «{settings.app_name}»!"}


@app.get("/info", tags=["Сервис"], summary="Получить информацию о сервисе")
def info(config: SettingsDep, repository: OrderRepositoryDep) -> dict[str, str | int]:
    """Возвращает название сервиса и число заказов в базе."""
    return {"name": config.app_name, "orders_count": len(repository.get_all())}
