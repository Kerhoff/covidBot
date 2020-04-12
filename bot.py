import COVID19Py, logging, requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#initialize covid
covid19 = COVID19Py.COVID19()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#initialize bot
updater = Updater(token='TOKEN', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def covid(update, context):
    latest = covid19.getLatest()
    message = f"Total:\n\nConfirmed: {latest['confirmed']}\n\nDeaths: {latest['deaths']}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    print(latest)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

covid_handler = CommandHandler('covid', covid)
dispatcher.add_handler(covid_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()

"""
location = covid19.getLocationByCountryCode('RU')
print(type(locations)) # locations is list
print(type(locations[0])) # location is dict
print(locations[0].keys()) # ['id', 'country', 'country_code', 'country_population', 'province', 'last_updated', 'coordinates', 'latest']
"""
