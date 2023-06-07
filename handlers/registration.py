import hashlib

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.exceptions import TelegramAPIError

import dispatcher
from dispatcher import dp
from bot import BotDB
from dispatcher import bot
from aiogram.dispatcher.filters.state import StatesGroup, State


# создание состояний для регистрации
class RegistrationStates(StatesGroup):
    USERNAME_INPUT = State()
    PASSWORD_INPUT = State()
    group_id = State()
    username = State()


class DeleteRegistrationStates(StatesGroup):
    confirm = State()


class LogoutStates(StatesGroup):
    confirm = State()


class LoginStates(StatesGroup):
    USERNAME_INPUT = State()
    PASSWORD_INPUT = State()
    username = State()
    confirm = State()


@dp.message_handler(commands=("logout"))
async def logout(message: types.Message):
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
    await message.answer("Вы действительно хотите выйти из учетной записи?", reply_markup=kb)
    await LogoutStates.confirm.set()


@dp.message_handler(state=LogoutStates.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        BotDB.logout(message.from_user.id)
        await message.answer("Вы успешно вышли из учетной записи.")
    else:
        await message.answer("Отменено.")
    await state.finish()


@dp.message_handler(commands=("delreg"))
async def reg(message: types.Message):
    if (BotDB.user_exists(message.from_user.id)):
        BotDB.delete_user(message.from_user.id)
        await message.answer(f"Пользователь удален!")
    else:
        await message.answer(f"Пользователь с таким id телеграмма не авторизован!")


@dp.message_handler(commands=("delreg"))
async def logout(message: types.Message):
    if (BotDB.user_exists(message.from_user.id)):
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
        await message.answer("Вы действительно хотите удалить свою учетную запись?", reply_markup=kb)
        await DeleteRegistrationStates.confirm.set()
    else:
        await message.answer(f"Пользователь с таким id телеграмма не авторизован!")


@dp.message_handler(state=DeleteRegistrationStates.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        BotDB.delete_user(message.from_user.id)
        await message.answer("Ваша учетная запись удалена.")
    else:
        await message.answer("Отменено.")
    await state.finish()


# обработчик команды регистрация
@dp.message_handler(commands=("login"))
async def process_login_command(message: types.Message):
    # вывод списка групп из базы данных
    if (not BotDB.user_exists(message.from_user.id)):
        await message.answer('Введите ваше ФИО:')
        await LoginStates.USERNAME_INPUT.set()
    else:
        await message.answer(f"Пользователь с таким id телеграмма авторизован!")


# обработчик ввода имени пользователя
@dp.message_handler(state=LoginStates.USERNAME_INPUT)
async def login_input_username_(message: types.Message, state: FSMContext):
    username = message.text
    await state.update_data(username=username)
    await message.answer('Введите ваш пароль (пароль будет удален из истории):')
    # устанавливаем состояние ввода пароля
    await LoginStates.PASSWORD_INPUT.set()


# обработчик ввода пароля
@dp.message_handler(state=LoginStates.PASSWORD_INPUT)
async def login_input_password(message: types.Message, state: FSMContext):
    password = message.text
    password = password.encode('utf-8')
    await bot.delete_message(message.chat.id, message.values.get('message_id'))
    await message.answer("Сообщение с паролем 🗑️Удалено")
    hashed_password = hashlib.sha256(password).hexdigest()
    data = await state.get_data()
    username = data.get('username')

    user_id = BotDB.find_by_user_fio_and_password(username, hashed_password)
    if not user_id is None:
        BotDB.login_by_id(user_id[0], message.from_user.id)
        await message.answer('Вход выполнен успешно!')
    else:
        await message.answer('Пользователь с таким ФИО и паролем не найден!')
    # завершаем процесс регистрации и сбрасываем состояние
    await state.finish()


# обработчик команды регистрация
@dp.message_handler(commands=("registration", "r", "reg"))
async def process_register_command(message: types.Message):
    # вывод списка групп из базы данных
    if (not BotDB.user_exists(message.from_user.id)):
        groups = BotDB.getAllGroupName()
        keyboard = types.InlineKeyboardMarkup()
        for group in groups:
            button = types.InlineKeyboardButton(text=group[1], callback_data=f'select_group_{group}')
            keyboard.add(button)
        await message.answer('Выберите вашу группу:', reply_markup=keyboard)
    else:
        await message.answer(f"Пользователь с таким id телеграмма уже авторизован!")


# Обработка нажатия на кнопку с группой
@dp.callback_query_handler(lambda c: c.data.startswith('select_group_'))
async def select_group(callback_query: types.CallbackQuery, state: FSMContext):
    group = callback_query.data.split('_')[-1]
    group_id = group[1:group.index(',')]
    await state.update_data(group_id=group_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f'Вы выбрали группу {group[1]}. Напишите Ваши фамилия, имя, отчество (Иванов Иван Иванович):')
    await RegistrationStates.USERNAME_INPUT.set()


# обработчик ввода имени пользователя
@dp.message_handler(state=RegistrationStates.USERNAME_INPUT)
async def input_username(message: types.Message, state: FSMContext):
    username = message.text
    if (not BotDB.user_exists_by_name(username)):
        await state.update_data(username=username)
        await message.answer('Введите ваш пароль (пароль будет удален из истории):')
        # устанавливаем состояние ввода пароля
        await RegistrationStates.PASSWORD_INPUT.set()
    else:
        await message.answer('Пользователь с таким ФИО уже существует!')
        await state.finish()


# обработчик ввода пароля
@dp.message_handler(state=RegistrationStates.PASSWORD_INPUT)
async def input_password(message: types.Message, state: FSMContext):
    password = message.text
    password = password.encode('utf-8')
    await bot.delete_message(message.chat.id, message.values.get('message_id'))
    await message.answer("Сообщение с паролем 🗑️Удалено")
    hashed_password = hashlib.sha256(password).hexdigest()
    data = await state.get_data()
    group_id = data.get('group_id')
    username = data.get('username')

    # сохраняем данные пользователя в базу данных
    BotDB.save_user(group_id, username, hashed_password, message.from_user.id)
    await message.answer('Регистрация завершена!', reply_markup=types.ReplyKeyboardRemove())
    # завершаем процесс регистрации и сбрасываем состояние
    await state.finish()
