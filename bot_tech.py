from bot import bot
from start import welcome_or_menu
from messages import TECH


@bot.message_handler(content_types=['text'])
def tech(msg):
  welcome_or_menu(msg.chat.id, TECH)

bot.remove_webhook()
bot.polling(none_stop=True)