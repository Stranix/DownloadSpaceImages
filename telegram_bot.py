import os
import random
import time

from telegram import Bot
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass


@dataclass
class SpaceImage:
    name: str
    path: Path


def send_photo_to_tg_channel(bot_token: str, chat_id: int, image: SpaceImage):
    bot = Bot(token=bot_token)
    bot.send_photo(chat_id, open(image.path.joinpath(image.name), 'rb'))


def get_images_from_folder(folder_to_scan: Path) -> list[SpaceImage]:
    images_for_send = []
    for scan_result in os.walk(folder_to_scan):
        images = scan_result[2]
        if not images:
            continue
        path_folder = scan_result[0]
        for image in images:
            images_for_send.append(SpaceImage(image, Path(path_folder)))
    return images_for_send


if __name__ == '__main__':
    load_dotenv()
    BOT_TOKEN = os.environ.get('BOT_TOKEN')

    while True:
        scan_folder = Path('./images')
        images = get_images_from_folder(scan_folder)
        random.shuffle(images)
        for image_to_send in images:
            send_photo_to_tg_channel(BOT_TOKEN, -1001902840562, image_to_send)
            time.sleep(14400)
