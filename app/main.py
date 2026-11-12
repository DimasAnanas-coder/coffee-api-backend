from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .config import get_settings
from .dependencies import OrderRepositoryDep, SettingsDep
from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .routers import orders, users
from .user_exceptions import UserAlreadyExistsError, UserNotFoundError

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Сервис учёта пользователей и заказов в PostgreSQL.",
    version="1.0.0",
)
app.include_router(orders.router)
app.include_router(users.router)


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request: Request, exc: OrderNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Заказ с id={exc.order_id} не найден"},
    )


@app.exception_handler(OrderAlreadyCompletedError)
async def order_already_completed_handler(request: Request, exc: OrderAlreadyCompletedError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"Заказ {exc.order_id} уже выполнен и не может быть изменён"},
    )


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    detail = f"Пользователь с id={exc.user_id} не найден" if exc.user_id is not None else f"Пользователь {exc.email} не найден"
    return JSONResponse(status_code=404, content={"detail": detail})


@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": f"Пользователь с email={exc.email} уже существует"})


@app.get("/", tags=["Сервис"], summary="Проверить работу сервиса")
def root() -> dict[str, str]:
    """Возвращает приветственное сообщение."""
    return {"message": f"Добро пожаловать в сервис «{settings.app_name}»!"}


@app.get("/info", tags=["Сервис"], summary="Получить информацию о сервисе")
def info(config: SettingsDep, repository: OrderRepositoryDep) -> dict[str, str | int]:
    """Возвращает название сервиса и число заказов в базе."""
    return {"name": config.app_name, "orders_count": len(repository.get_all())}
