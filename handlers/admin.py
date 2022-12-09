from aiogram import types
from aiogram.dispatcher import FSMContext
from dispatcher import dp
from bot import BotDB
from config import ADMINS_ID
from states import adminStates


@dp.message_handler(commands=("ahelp"))
async def ahelp(message: types.Message):
    flag = False
    for admin in ADMINS_ID:
        if message.from_user.id == admin:
            flag = True
    if flag:
        await message.answer(f"add")


@dp.message_handler(commands=("qadd"))
async def qadd(message: types.Message):
    flag = False
    for admin in ADMINS_ID:
        if message.from_user.id == admin:
            flag = True
    if flag:
        await message.answer(f"Вы начали добавление нового вопроса в БД. \nВведите вопрос: ")
        await adminStates.quiest.set()


@dp.message_handler(state=adminStates.quiest)
async def addquest(message: types.Message, state: FSMContext):
    quest = message.text
    if len(quest):
        await message.answer(f"Question: {quest}")
        await state.update_data(quest=quest)
        await message.answer(f"Введите ответ: ")
        await adminStates.answer.set()
    else:
        await message.reply("Не введен вопрос!")
        await state.finish()


@dp.message_handler(state=adminStates.answer)
async def addanswer(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer):
        await message.answer(f"Ответ: {answer}")
        await state.update_data(answer=answer)
        data = await state.get_data()
        quest = data.get('quest')
        # ЗАПРОС!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        await state.finish()
    else:
        await message.reply("Не введен ответ!")
        await state.finish()
