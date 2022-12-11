from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from states import registration
from dispatcher import dp
from bot import BotDB

@dp.message_handler(commands=("registration", "r", "reg"))
async def reg(message: types.Message):
    if (not BotDB.user_exists(message.from_user.id)):
        list_groups = BotDB.get_groups()
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for i in list_groups:
            for j in i:
                kb.add(KeyboardButton(j))
        await message.answer(f"Выберите свою группу", reply_markup= kb)
        await registration.group.set()
    else:
        await message.answer(f"Пользователь с таким id телеграмма уже создан!")

@dp.message_handler(state=registration.group)
async def get_group(message: types.Message, state: FSMContext):
    global list
    await state.update_data(group=message.text)
    list_students = BotDB.get_students(message.text)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in list_students:
        for j in i:
            kb.add(KeyboardButton(j))

    await message.answer(f"Выберите свое имя", reply_markup=kb)
    await registration.name.set()
@dp.message_handler(state=registration.name)
async def get_name(message: types.Message, state: FSMContext):
    temp = message.text
    if temp == 'Отменить':
        await state.finish()
    else:
        id = BotDB.find_user2(message.text)
        BotDB.add_user2(message.from_user.id, id)
        await message.answer(f"Пользователь добавлен!")
        #!Закрывает state!
        await state.finish()
