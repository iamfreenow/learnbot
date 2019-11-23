from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Hello {}'.format(emo)
    update.message.reply_text(text, reply_markup=get_keyboard)


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Hello {} {}!, You have written: {}".format(update.message.chat.first_name, emo,
                                                            update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
        emo = get_user_emo(user_data)
        update.message.reply_text('Done: {}'.format(emo), reply_markup=get_keyboard())


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Done: {}'.format(get_user_emo(user_data), reply_markup=get_keyboard()))


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Done: {}'.format(get_user_emo(user_data), reply_markup=get_keyboard()))


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def get_keyboard():
    contact_button = KeyboardButton('Send contact', request_contact=True)
    contact_location = KeyboardButton('Send location', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Send ma a cat', 'Change my avatar'],
                                        [contact_button, contact_location],
                                       ], resize_keyboard=True
                                      )
    return my_keyboard


def main():

    super_bot = Updater(settings.API_KEY)  # use_context=True
    logging.info('The bot is running')

    sb = super_bot.dispatcher
    sb.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    sb.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
    sb.add_handler(MessageHandler(Filters.regex('(Send me a cat)'), send_cat_picture, pass_user_data=True))
    sb.add_handler(MessageHandler(Filters.regex('(Change my avatar)'), change_avatar, pass_user_data=True))
    sb.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    sb.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    sb.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))

    super_bot.start_polling()
    super_bot.idle()


main()
