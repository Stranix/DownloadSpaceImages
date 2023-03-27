import os
import urllib
import requests
import argparse

from dotenv import load_dotenv
from services import download_image


def create_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-count', '-c', '--image_count', type=int, default=1)

    return arg_parser


def fetch_apod_images(api_key: str = 'DEMO_KEY', image_count: int = 1):
    apod_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': image_count
    }

    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    response_data = response.json()

    images_url = [data['url'] for data in response_data]

    for counter, image_url in enumerate(images_url):
        ext = get_file_ext_from_url(image_url)

        if ext not in ['.jpeg', '.jpg', '.png', '.gif']:
            continue

        image_name = f'nasa_apod_{counter}{ext}'
        download_image(image_url, './images/apod', image_name)


def get_file_ext_from_url(url: str) -> str:
    split_result = urllib.parse.urlsplit(url)
    url_path = split_result.path
    file_ext = os.path.splitext(url_path)[-1]

    return file_ext


def main():
    load_dotenv()
    nasa_token = os.environ.get('NASA_TOKEN')
    parser = create_arg_parser()
    namespace = parser.parse_args()

    fetch_apod_images(nasa_token, namespace.image_count)


if __name__ == '__main__':
    main()
