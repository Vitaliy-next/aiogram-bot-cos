from aiogram.fsm.state import StatesGroup, State


class ClientsAccess(StatesGroup):
    waiting_clients_password = State()
    waiting_orders_password = State()



