from aiogram.dispatcher.filters.state import StatesGroup, State

class adminStates(StatesGroup):
    quiest = State()
    answer = State()