from aiogram.dispatcher.filters.state import StatesGroup, State

class adminStates(StatesGroup):
    quest = State()
    answer = State()
    message = State()