import logging, requests, json
from COVID19Py import COVID19
from config import token
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from telegram import ParseMode, ChatAction, ReplyKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

covid19 = COVID19()
data = dict()

def get_latest_data():
    global data 
    data = covid19.getAll()

def start(update, context):
    bot_keyboard = [['covid', 'top-right'], 
                        ['bottom-left', 'bottom-right']]
    reply_markup = ReplyKeyboardMarkup(bot_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                 text="I'm a bot, please talk to me!", 
                 reply_markup=reply_markup)

def reply_to_message(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    text = update.message.text
    
    if (not bool(data)):
        get_latest_data()

    if text == 'covid':
        covid_keyboard = [['latest', 'Russia'],
                        ['main menu']]
        reply_markup = ReplyKeyboardMarkup(covid_keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, 
                     text="You are in COVID19 menu", 
                     reply_markup=reply_markup)
    elif text == 'latest':
        latest = data['latest']
        message = f"*Total:*\nConfirmed: {latest['confirmed']:,}\nDeaths: {latest['deaths']:,}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN_V2)
    elif text == 'main menu':
        main_keyboard = [['covid', 'top-right'], 
                        ['bottom-left', 'bottom-right']]
        reply_markup = ReplyKeyboardMarkup(main_keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, 
                 text="You are in the main menu.", 
                 reply_markup=reply_markup)
    else:
        message = text
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN_V2)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def bot():
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    """covid_handler = CommandHandler('covid', covid)
    dispatcher.add_handler(covid_handler)"""

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    message_handler = MessageHandler(Filters.text, reply_to_message)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    bot()