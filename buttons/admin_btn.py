from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = KeyboardButton('Upload')
button_delete = KeyboardButton('Delete')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.row(button_load, button_delete)
