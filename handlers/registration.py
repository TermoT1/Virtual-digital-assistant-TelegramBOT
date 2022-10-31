from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dispatcher import dp
from states import registration
from dispatcher import dp

@dp.message_handler(commands=("registration", "r", "reg"))
async def reg(message: types.Message):
    group_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'ПИЭ-19')
            ],
            [
                KeyboardButton(text=f'ПИЭ-21')
            ],
            [
                KeyboardButton(text=f'Отменить')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"Выберите свою группу", reply_markup= group_kb)
    await registration.group.set()

@dp.message_handler(state=registration.group)
async def get_group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    name_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'Студент1')
            ],
            [
                KeyboardButton(text=f'Студент2')
            ],
            [
                KeyboardButton(text=f'Студент3')
            ],
            [
                KeyboardButton(text=f'<k>Отменить<k>')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"Выберите свое имя", reply_markup=name_kb)
    await registration.name.set()
    #await message.answer(f'<b>{message.text}')
@dp.message_handler(state=registration.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
