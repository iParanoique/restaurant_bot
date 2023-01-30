from aiogram import types, Dispatcher
from buttons import kb_client
from data_base import sqlite_db


async def command_start(message: types.Message):
    await message.answer('Hey there! You are Welcome :)', reply_markup=kb_client)


async def command_hours(message: types.Message):
    await message.answer('Mon - Fri [9:00 - 21:00]\nSat, Sun [10:00 - 20:00]')


async def command_location(message: types.Message):
    await message.answer('Kyiv, street Dragomanova 6')


async def command_menu(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_hours, text='Working hours')
    dp.register_message_handler(command_location, text='Location')
    dp.register_message_handler(command_menu, text='Menu')
