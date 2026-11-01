from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .config import get_settings
from .dependencies import SettingsDep
from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .dependencies import get_repository
from .routers import orders

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Сервис учёта заказов кофейни. Данные хранятся в памяти процесса.",
    version="1.0.0",
)
app.include_router(orders.router)


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


@app.get("/", tags=["Сервис"], summary="Проверить работу сервиса")
def root() -> dict[str, str]:
    """Возвращает приветственное сообщение."""
    return {"message": f"Добро пожаловать в сервис «{settings.app_name}»!"}


@app.get("/info", tags=["Сервис"], summary="Получить информацию о сервисе")
def info(config: SettingsDep) -> dict[str, str | int]:
    """Возвращает название сервиса и число заказов в памяти."""
    repository = get_repository()
    return {"name": config.app_name, "orders_count": len(repository.get_all())}
