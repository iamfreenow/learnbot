from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



def talk_to_me(bot, update):
     user_text = "Hello {}!, You have written: {}".format(update.message.chat.first_name,update.message.text)
     logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, update.message.chat.id,
                    update.message.text)
     update.message.reply_text(user_text)


def greet_user(bot, update):
    text = 'Pressed /start'
    logging.info(text)
    update.message.reply_text(text)


def main():
    superbot = Updater(settings.API_KEY)
    
    logging.info('The bot is running')

    sb = superbot.dispatcher
    sb.add_handler(CommandHandler('start', greet_user))
    sb.add_handler(MessageHandler(Filters.text, talk_to_me))

    superbot.start_polling()
    superbot.idle()


main()

