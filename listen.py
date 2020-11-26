from bot import bot
from telebot import types
from config import BITS_TYPES, StatesList, DB_NAME
from states_db_worker import States
from sql_worker import SQL
from start import welcome_or_menu


def to_listen(msg):
  try:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    [keyboard.add(bit_type) for bit_type in BITS_TYPES]

    bot.send_message(msg.chat.id, 'Выберите стиль', reply_markup=keyboard)
    States.set_state(msg.chat.id, StatesList.LISTEN.value)
  except Exception as e:
    print(e)
    bot.send_message(msg.chat.id, 'Error')


def check_types(msg):
  try:
    if msg.text in BITS_TYPES:
      database = SQL(DB_NAME)
      bits = database.get_bits(msg.text)
      database.close()

      if len(bits) > 0:
        for bit in bits:
          bot.send_audio(msg.chat.id, bit[1])

        welcome_or_menu(msg.chat.id, 'Окей, что будешь делать дальше? 😎')
      else:
        welcome_or_menu(msg.chat.id, 'Пока нет треков такого стиля 😢')
    else:
      bot.send_message(msg.chat.id, 'Ты что делаеш?')
  except Exception as e:
    print(e)
    bot.send_message(msg.chat.id, 'Error')