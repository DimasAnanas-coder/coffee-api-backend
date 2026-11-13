from decimal import Decimal

from sqlalchemy.orm import Session

from ..exceptions.order import InsufficientBalanceError
from ..exceptions.user import UserNotFoundError
from ..infrastructure.repository.order import OrderRepository
from ..infrastructure.repository.user import UserRepository
from ..schemas import Order, OrderCreate, OrderStatus


class CreateOrderUseCase:
    """Создаёт заказ и списывает баланс в одной транзакции."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.orders = OrderRepository(session)

    def execute(self, order_data: OrderCreate) -> Order:
        amount = Decimal(order_data.amount)
        if amount <= 0:
            raise ValueError("Сумма заказа должна быть положительной")

        with self.session.begin():
            user = self.users.get_by_id_for_update(order_data.user_id)
            if user is None:
                raise UserNotFoundError(user_id=order_data.user_id)
            if user.balance < amount:
                raise InsufficientBalanceError(order_data.user_id)

            self.users.set_balance(user.id, user.balance - amount)
            order = self.orders.add(order_data)
            return order.model_copy(update={"status": OrderStatus.pending})
