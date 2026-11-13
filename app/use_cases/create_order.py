from decimal import Decimal

from ..exceptions.order import InsufficientBalanceError
from ..exceptions.user import UserNotFoundError
from ..ports import UnitOfWorkProtocol
from ..schemas import Order, OrderCreate, OrderStatus


class CreateOrderUseCase:
    """Создаёт заказ и списывает баланс в одной транзакции."""

    def __init__(self, uow: UnitOfWorkProtocol) -> None:
        self.uow = uow

    def execute(self, order_data: OrderCreate) -> Order:
        amount = Decimal(order_data.amount)
        if amount <= 0:
            raise ValueError("Сумма заказа должна быть положительной")

        with self.uow:
            user = self.uow.users.get_by_id_for_update(order_data.user_id)
            if user is None:
                raise UserNotFoundError(user_id=order_data.user_id)
            if user.balance < amount:
                raise InsufficientBalanceError(order_data.user_id)

            self.uow.users.set_balance(user.id, user.balance - amount)
            order = self.uow.orders.add(order_data)
            return order.model_copy(update={"status": OrderStatus.pending})
