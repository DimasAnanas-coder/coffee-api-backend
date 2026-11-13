class OrderNotFoundError(Exception):
    def __init__(self, order_id: int) -> None:
        self.order_id = order_id
        super().__init__(order_id)


class OrderAlreadyCompletedError(Exception):
    def __init__(self, order_id: int) -> None:
        self.order_id = order_id
        super().__init__(order_id)


class InsufficientBalanceError(Exception):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(user_id)
