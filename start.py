from telebot import types
from bot import bot
from messages import LISTEN, BUY, ADD
from config import StatesList, DB_NAME
from states_db_worker import States


def welcome_or_menu(chat_id, text):
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.add(LISTEN)
  keyboard.add(BUY)

  if chat_id == 551443480 or chat_id == 623849739:
    keyboard.add(ADD)

  bot.send_message(chat_id, text, reply_markup=keyboard)
  States.set_state(chat_id, StatesList.START.value)