from ChatGPT_HKBU import ChatGPT
gpt = None
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import configparser
import logging

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logging.info('INIT: Loading configuration...')
    config = configparser.ConfigParser()
    config.read('config.ini')
    global gpt
    gpt = ChatGPT(config)


    logging.info('INIT: Connecting the Telegram bot...')
    app = ApplicationBuilder().token(
        config['TELEGRAM']['ACCESS_TOKEN']
    ).build()

    logging.info('INIT: Registering the message handler...')
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, callback)
    )

    logging.info('INIT: Initialization done!')
    app.run_polling()

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("UPDATE: " + str(update))

    loading_message = await update.message.reply_text('Thinking...')

    response = gpt.submit(update.message.text)

    await loading_message.edit_text(response)


if __name__ == '__main__':
    main()


