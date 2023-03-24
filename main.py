import os
import argparse

from dotenv import load_dotenv

from download_spacex_images import fetch_spacex_launch
from download_apod_images import download_apod_images
from download_epic_images import download_epic_images


def create_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-id', '--launch_id', default='latest')
    arg_parser.add_argument('-c', '--apod_image_count', type=int, default=1)

    return arg_parser


if __name__ == '__main__':
    load_dotenv()
    nasa_token = os.environ.get('NASA_TOKEN')
    parser = create_arg_parser()
    namespace = parser.parse_args()

    fetch_spacex_launch(namespace.launch_id)
    download_apod_images(nasa_token, namespace.apod_image_count)
    download_epic_images(nasa_token)
