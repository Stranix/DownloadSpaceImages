import os

from telegram import Bot
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    bot = Bot(token=BOT_TOKEN)
