import os
import random
import time
import argparse

from telegram import Bot
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass


@dataclass
class SpaceImage:
    name: str
    path: Path


def create_arg_parser():
    description = 'Публикуем фото из папки в Телеграм'
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('-img', '--images', default='./images', metavar='',
                            help='''Путь до папки с фотографиями для публикации или до файла картинки. По умолчанию 
                            ищем фото в папке ./images'''
                            )

    return arg_parser


def send_photo_to_tg_channel(tg_bot_token: str, tg_chat_id: int, image: Path):
    bot = Bot(token=tg_bot_token)
    bot.send_photo(tg_chat_id, image.read_bytes())


def get_images_from_folder(folder_to_scan: Path) -> list[SpaceImage]:
    images_for_send = []
    for path_folder, sub_folders, images in os.walk(folder_to_scan):
        if not images:
            continue

        for image in images:
            images_for_send.append(SpaceImage(image, Path(path_folder)))

    return images_for_send


def publish_photos_from_folders(folder: Path, tg_bot_token: str, tg_chat_id: int, post_timeout: int = 14400):
    while True:
        images = get_images_from_folder(folder)

        if not images:
            print('Нет фото для публикаций. Загрузите фото и попробуйте снова.')
            break

        random.shuffle(images)
        for image in images:
            image.path.joinpath(image.name)
            send_photo_to_tg_channel(tg_bot_token, tg_chat_id, image.path.joinpath(image.name))
            time.sleep(post_timeout)


def main():
    load_dotenv()
    parser = create_arg_parser()
    args = parser.parse_args()

    bot_token = os.environ.get('TG_BOT_TOKEN')
    timeout = int(os.environ.get('TG_POST_TIMEOUT'))
    chat_id = int(os.environ.get('TG_CHAT_ID'))

    if Path(args.images).is_file():
        send_photo_to_tg_channel(bot_token, chat_id, Path(args.images))
    else:
        publish_photos_from_folders(Path(args.images), bot_token, chat_id, timeout)


if __name__ == '__main__':
    main()
