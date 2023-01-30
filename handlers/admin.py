from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from buttons import admin_btn
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ID = None


class FSKAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Root verified', reply_markup=admin_btn.kb_admin)
    await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSKAdmin.photo.set()
        await message.answer('Photo')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('Canceled!')


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSKAdmin.next()
        await message.answer('Name')


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSKAdmin.next()
        await message.answer('Description')


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSKAdmin.next()
        await message.answer('Price')


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()


async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} deleted.', show_alert=True)


async def command_delete(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0],
                                 f'{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                       f'Delete {ret[1]}', callback_data=f'del {ret[1]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, text='Upload', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSKAdmin.photo)
    dp.register_message_handler(load_name, state=FSKAdmin.name)
    dp.register_message_handler(load_description, state=FSKAdmin.description)
    dp.register_message_handler(load_price, state=FSKAdmin.price)
    dp.register_message_handler(command_delete, text='Delete')
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
    dp.register_callback_query_handler(del_callback_run,
                                       lambda x: x.data and x.data.startswith('del '))
