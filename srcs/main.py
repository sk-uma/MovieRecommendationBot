from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import dotenv_values
from get_ranking import get_ranking
from reply_message import reply_message

temp = dotenv_values(".env")
TOKEN = temp["TELEGRAM_APIKEY"]

# update.message.reply_text(TEXT_MESSAGE)
# update.message.reply_photo(URL)


class SampleBot:
    def __init__(self):
        self.counter = 0

    def start(self, bot, update):
        update.message.reply_text('''こんにちは！本サービスをご利用いただきありがとうございます。
あなたの観たい映画について教えてください''')

    def message(self, bot, update):
        print('カウンター：', self.counter)

        if self.counter == 0:
            user_input = update.message.text
            update.message.reply_text('そんなあなたにオススメの映画はこちらです！')
            reply_message(user_input, update)

    def run(self):
        updater = Updater(TOKEN)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(MessageHandler(Filters.text, self.message))
        dp.add_handler(MessageHandler(Filters.photo, self.message))
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    mybot = SampleBot()
    mybot.run()
