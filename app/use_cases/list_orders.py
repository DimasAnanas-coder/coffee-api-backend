from ..ports import UnitOfWorkProtocol
from ..schemas import Order, OrderStatus


class ListOrdersUseCase:
    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(
        self,
        order_status: OrderStatus | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Order]:
        return self.uow.orders.get_all(order_status=order_status, limit=limit, offset=offset)
