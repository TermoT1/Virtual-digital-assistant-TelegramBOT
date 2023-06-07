from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from states import registration
from dispatcher import dp
from bot import BotDB
from dispatcher import bot
from config import ADMINS_ID
from config import URL_SCHEDULE
from states import adminStates
import datetime

@dp.message_handler(commands=("books", "книги"), commands_prefix="/!")
async def schedule(message: types.Message):
    if (BotDB.user_exists(message.from_user.id)):
        books_str = ""
        books_str += "📕Базы данных:" + '\n'
        books_str += "🔴 Введение в системы баз данных К. Дж.Дейт" + '\n' + \
                     "🔴 MySQL по максимуму Бэрон Шварц, Вадим Ткаченко, Петр Зайцев" + '\n' + \
                     "🔴 Семь баз данных за семь недель Джим Р. Уилсон, Эрик Редмонд" + '\n'
        books_str += '\n'
        books_str += '📗Программная инженерия' + '\n'
        books_str += "🟢Книга «Программная инженерия. Учебник для вузов. 5-е издание обновленное и дополненное»"
        await message.bot.send_message(message.from_user.id, books_str)
    else:
        await message.reply("Пройдите регистрацию /reg \nИли войдите в свой аккаунт /login")

@dp.message_handler(commands=("schedule", "расписание"), commands_prefix="/!")
async def schedule(message: types.Message):
    if (BotDB.user_exists(message.from_user.id)):
        group = BotDB.get_group_by_user_id(message.from_user.id)
        str = "Ссылка на расписание вашей группы: " + URL_SCHEDULE + group
        # определяем текущую дату
        today = datetime.date.today()
        # определяем номер недели в году (ISO-формат)
        week_number = today.isocalendar()[1]
        # проверяем, четная ли неделя
        if week_number % 2 == 0:
            week = "Сейчас идет четная неделя"
        else:
            week = "Сейчас идет нечетная неделя"
        str += "\n" + week
        await message.bot.send_message(message.from_user.id, str)
    else:
        await message.reply("Пройдите регистрацию /reg \nИли войдите в свой аккаунт /login")

@dp.message_handler(commands=("question", "quest", "q"), commands_prefix="/!")
async def quest(message: types.Message):
    if BotDB.user_exists(message.from_user.id):
        answer = ""
        cmd_variants = (('/question', '/quest', '/q',))
        question = message.text
        for i in cmd_variants:
            question = question.replace(i, '').strip()
        if len(question):
            await message.answer(f"Question: {question}")
            answer = BotDB.answer_question(question)
        else:
            await message.reply("Пустой вопрос!")
        if len(answer):
            str = answer[0]
            await message.answer(f"Ответ: {str[0]}")
        else:
            await message.reply("Ответ не найден!")
            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=f'Да')
                    ],
                    [
                        KeyboardButton(text=f'Нет')
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
            #Глобальная переменная для передачи question дальше
            global unfound_question
            unfound_question = question
            await message.answer(f"Хотели бы вы отправить уведомление преподавателю?", reply_markup=kb)
            global name_student
            name_student = BotDB.get_user_by_id_my(message.from_user.id)
            await adminStates.message.set()
    else:
        await message.reply("Пройдите регистрацию /reg \nИли войдите в свой аккаунт /login")


@dp.message_handler(state=adminStates.message)
async def message_admin(message: types.Message, state: FSMContext):
    str = message.text
    if str == "Да":
        strr = f"Уведомление от пользователя {name_student} с id {message.from_user.id}:\n" \
              f"Не найден ответ на вопрос:\n" + unfound_question
        for admin in ADMINS_ID:
            await bot.send_message(admin, strr)
        await state.finish()
    elif str == "Нет":
        await state.finish()
    else:
        await message.answer("Ошибка ввода!")
        await state.finish()


@dp.message_handler(commands=("qid"), commands_prefix="/!")
async def select_by_id(message: types.Message):
    if (BotDB.user_exists(message.from_user.id)):
        cmd_variants = (('/qid', '/QID'))
        id = message.text
        for i in cmd_variants:
            for j in i:
                id = id.replace(j, '').strip()

        if len(id):
            qst_answr = BotDB.answer_question_by_id(id)
        else:
            await message.reply("Не введен id!")

        if len(qst_answr):
            i = qst_answr[0]
            await message.answer(f"Id: {i[0]}")
            await message.answer(f"Вопрос: {i[1]}")
            await message.answer(f"Ответ: {i[2]}")
        else:
            await message.reply("Запись не найдена!")
    else:
        await message.reply("Пройдите регистрацию! /reg")


@dp.message_handler(commands=("m"), commands_prefix="/!")
async def message(message: types.Message):
    if (BotDB.user_exists(message.from_user.id)):
        cmd_variants = (('/m', '/M'))
        mess = message.text
        for i in cmd_variants:
            for j in i:
                mess = mess.replace(j, '').strip()
        if len(mess):
            global name_student
            name_student = BotDB.get_group_by_user_id2(message.from_user.id)
            str = f"Сообщение от студента {name_student[0]} с id {message.from_user.id}:\n"
            for admin in ADMINS_ID:
                await bot.send_message(admin, str + mess)
        else:
            await message.reply("Пустое сообщение!")
    else:
        await message.reply("Пройдите регистрацию! /reg")


