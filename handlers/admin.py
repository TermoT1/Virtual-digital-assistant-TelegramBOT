from aiogram import types
from aiogram.dispatcher import FSMContext
from dispatcher import dp
from bot import BotDB
from config import ADMINS_ID
from states import adminStates


@dp.message_handler(commands = ("question", "quest", "q"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = (('/question', '/quest', '/q'))
    question = message.text
    for i in cmd_variants:
        for j in i:
            question = question.replace(j, '').strip()

    if len(question):
        await message.answer(f"Question: {question}")
        answer = BotDB.answer_question(question)
    else:
        await message.reply("Пустой вопрос!")

    if len(answer):
        await message.answer(f"Ответ: {answer}.")
    else:
        await message.reply("Ответ не найден!")

@dp.message_handler(commands = ("qdelete"), commands_prefix = "/!")
async def qdelete(message: types.Message):
    flag = False
    for admin in ADMINS_ID:
        if message.from_user.id == admin:
            flag = True
    if flag:
        cmd_variants = (('/qdelete'))
        id = message.text
        id = id.replace(cmd_variants, '').strip()
        if len(id):
            #Если выборка из БД не пустая, запись c таким id существует
            if int(len(BotDB.answer_question_by_id(id))):
                await message.answer(f"id удаляемой записи: {id}")
                BotDB.delete_answer_question(id)
                await message.answer(f"Запись в БД с id:{id} удалена!")
            else:
                await message.answer(f"Запись в БД с id:{id} не найдена!")
        else:
            await message.reply("Введите id!")
    else:
        await message.reply("Не администартор!")


@dp.message_handler(commands=("qadd"))
async def qadd(message: types.Message):
    flag = False
    for admin in ADMINS_ID:
        if message.from_user.id == admin:
            flag = True
    if flag:
        await message.answer(f"Вы начали добавление нового вопроса в БД. \nВведите вопрос: ")
        await adminStates.quest.set()
    else:
        await message.reply("Не администартор!")


@dp.message_handler(state=adminStates.quest)
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
        BotDB.add_answer_question(quest, answer)
        await message.reply("Запись в БД добавлена.")
        await state.finish()
    else:
        await message.reply("Не введен ответ!")
        await state.finish()
