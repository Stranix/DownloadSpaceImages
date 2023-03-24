import requests
import argparse
from services import download_image


def create_arg_parser():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-id', '--launch_id', default='latest')

    return arg_parser


def fetch_spacex_launch(launch_id: str = 'latest'):

    launch_url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(launch_url)
    response.raise_for_status()
    response_data = response.json()
    space_x_images_url = response_data['links']['flickr']['original']

    if not space_x_images_url:
        print('У последнего запуска нет фото :(')
        print('Попробуйте передать id запуска с помощью ключа -id')

    for counter, image_url in enumerate(space_x_images_url):
        image_name = f'spacex_{launch_id}_{counter}.jpg'
        download_image(image_url, './images', image_name)


if __name__ == '__main__':

    parser = create_arg_parser()
    namespace = parser.parse_args()

    fetch_spacex_launch(namespace.launch_id)
