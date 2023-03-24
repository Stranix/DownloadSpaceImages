import os

from telegram import Bot
from dotenv import load_dotenv
from pathlib import Path

if __name__ == '__main__':
    load_dotenv()
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    bot = Bot(token=BOT_TOKEN)
    chat_id = -1001902840562

    path_to_image = Path('./images/nasa_apod_4.jpg')
    bot.send_photo(chat_id, open(path_to_image, 'rb'))
