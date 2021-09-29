from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import dotenv_values

temp = dotenv_values(".env")
TOKEN = temp["TELEGRAM_APIKEY"]

# update.message.reply_text(TEXT_MESSAGE)
# update.message.reply_photo(URL)


class SampleBot:
    def __init__(self):
        self.counter = 0

    def start(self, bot, update):
        update.message.reply_text('''開始メッセージ（あとで考える）''')

    def message(self, bot, update):
        print('カウンター：', self.counter)

        if self.counter == 0:
            user_input = update.message.text
            if '興行収入ランキング' in user_input:
                print('興行収入ランキングを表示')
                self.counter = 0
            else:
                print('推薦処理へ移行')

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
