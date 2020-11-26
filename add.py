from bot import bot
from telebot import types
from config import BITS_TYPES, StatesList, DB_NAME
from states_db_worker import States
from sql_worker import SQL
from start import welcome_or_menu
from messages import WHAT_A_U_DOING
import random

def to_add(msg):
  try:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    [keyboard.add(bit_type) for bit_type in BITS_TYPES]

    bot.send_message(msg.chat.id, 'Выберите стиль', reply_markup=keyboard)
    States.set_state(msg.chat.id, StatesList.ADD.value)
  except Exception as e:
    print(e)
    bot.send_message(msg.chat.id, 'Error')


def check_types(msg):
  try:
    if msg.text in BITS_TYPES:
      States.set_state(f'data-{msg.chat.id}', msg.text)

      keyboard = types.ReplyKeyboardRemove()
      bot.send_message(msg.chat.id, 'Загрузите бит', reply_markup=keyboard)
      States.set_state(msg.chat.id, StatesList.ADD_MUSIC_UPLOAD.value)
    else:
      bot.send_message(msg.chat.id, WHAT_A_U_DOING)
  except Exception as e:
    print(e)
    bot.send_message(msg.chat.id, 'Error')


def check_music(msg):
  try:
    database = SQL(DB_NAME)
    bit_type = States.get_state(f'data-{msg.chat.id}')
    database.add_bit(bit_type, msg.audio.file_id)
    database.close()

    rand = random.randint(1, 10)

    if rand > 2:
      welcome_or_menu(msg.chat.id, 'Готово 👍')
    elif rand == 1:
      welcome_or_menu(msg.chat.id, 'Лютик ховається від такого біта 💪')
    else:
      welcome_or_menu(msg.chat.id, 'Бодя Крупа підтверджує, шо біт просто пушка 🤯')

    bot.send_message(623849739, 'New beatz added')
  except Exception as e:
    print(e)
    bot.send_message(msg.chat.id, 'Error')