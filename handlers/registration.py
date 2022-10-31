from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from states import registration
from dispatcher import dp
from bot import BotDB

@dp.message_handler(commands=("registration", "r", "reg"))
async def reg(message: types.Message):
    if (not BotDB.user_exists(message.from_user.id)):
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
    else:
        await message.answer(f"Пользователь с таким id телеграмма уже создан!")

@dp.message_handler(state=registration.group)
async def get_group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    name_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'Важов Данил')
            ],
            [
                KeyboardButton(text=f'Шипилов Владислав')
            ],
            [
                KeyboardButton(text=f'Студент3')
            ],
            [
                KeyboardButton(text=f'Отменить')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"Выберите свое имя", reply_markup=name_kb)
    await registration.name.set()
@dp.message_handler(state=registration.name)
async def get_name(message: types.Message, state: FSMContext):
    id = BotDB.find_user(message.text)
    BotDB.add_user2(message.from_user.id, id)
    await message.answer(f"Пользователь добавлен!")

