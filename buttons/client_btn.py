from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

button_hours = KeyboardButton('Working hours')
button_location = KeyboardButton('Location')
button_menu = KeyboardButton('Menu')
button_share_phone = KeyboardButton('Call me', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(button_hours, button_location, button_share_phone).add(button_menu)
