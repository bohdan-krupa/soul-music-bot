import random
import time
import telebot
from flask import Flask, request
from bot import bot
from messages import *
from config import StatesList, DB_NAME, IS_DEPLOYED, WEBHOOK_URL, WEBHOOK_SECRET
from states_db_worker import States
from sql_worker import SQL
from start import welcome_or_menu
import listen
import add
  

@bot.message_handler(commands=['start'])
def welcome(msg):
  welcome_or_menu(msg.chat.id, WELCOME)
  

@bot.message_handler(func=lambda msg: States.get_state(msg.chat.id) == StatesList.START.value)
def main_menu_select(msg):
  if msg.text == LISTEN:
    listen.to_listen(msg)
  elif msg.text == BUY:
    inline = telebot.types.InlineKeyboardMarkup()
    inline.add(telebot.types.InlineKeyboardButton('Написать', url='https://t.me/sm1rtpeople'))

    bot.send_message(msg.chat.id, 'Напиши мне 🤝', reply_markup=inline)
  elif msg.text == ADD:
    add.to_add(msg)
  else:
    bot.send_message(msg.chat.id, 'Ты что делаеш?')


@bot.message_handler(func=lambda msg: States.get_state(msg.chat.id) == StatesList.LISTEN.value)
def listen_check_types(msg):
  listen.check_types(msg)


@bot.message_handler(func=lambda msg: States.get_state(msg.chat.id) == StatesList.ADD.value)
def add_check_types(msg):
  add.check_types(msg)


@bot.message_handler(content_types=['audio'], func=lambda msg: States.get_state(msg.chat.id) == StatesList.ADD_MUSIC_UPLOAD.value)
def add_check_music(msg):
  add.check_music(msg)


if IS_DEPLOYED:
  bot.remove_webhook()
  time.sleep(1)
  bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_SECRET)

  app = Flask(__name__)

  @app.route('/' + WEBHOOK_SECRET, methods=['POST'])
  def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])

    return 'ok', 200

  if __name__ == '__main__':
    app.run()
else:
  bot.remove_webhook()
  bot.polling(none_stop=True)