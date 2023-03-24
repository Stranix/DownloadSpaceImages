import os
import urllib
import datetime
import requests


from pathlib import Path
from dotenv import load_dotenv


class LimitEpicImages(Exception):

    def __init__(self, image_count, message='Можно загрузить не больше 13 фотографий'):
        self.image_count = image_count
        self.message = message
        super().__init__(self.message)


print('DEBUG __name__ :', __name__)


def get_list_epic_images_url(api_key: str = 'DEMO_KEY'):
    result = []
    url = 'https://api.nasa.gov/EPIC/api/natural?api_key=DEMO_KEY'
    params = {
        'api_key': api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_data = response.json()
    for data in response_data:
        image_date_time = datetime.datetime.fromisoformat(data['date'])
        image_date = datetime.date.strftime(image_date_time, '%Y/%m/%d')
        image_name = data['image'] + '.png'

        print('DEBUG image_date_time:', image_date_time)
        print('DEBUG image_date:', image_date)
        print('DEBUG image_name:', image_name)

        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}'
        result.append(image_url)

    return result


def download_epic_images(api_key: str = 'DEMO_KEY'):
    params = {
        'api_key': api_key
    }
    images_url = get_list_epic_images_url()
    for counter, url in enumerate(images_url):
        image_name = f'epic_{counter}.png'
        download_image(url, './images/epic', image_name, params)


def download_apod_images(api_key: str = 'DEMO_KEY', image_count: int = 1):
    apod_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': image_count
    }
    print(apod_url)
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    response_data = response.json()
    print(response_data)

    images_url = [data['url'] for data in response_data]
    print(images_url)
    for counter, image_url in enumerate(images_url):
        ext = get_file_ext_from_url(image_url)
        if ext not in ['.jpeg', '.jpg', '.png', '.gif']:
            continue
        image_name = f'nasa_apod_{counter}{ext}'
        download_image(image_url, './images/nasa', image_name)


def get_file_ext_from_url(url: str) -> str:
    split_result = urllib.parse.urlsplit(url)
    url_path = split_result.path
    file_ext = os.path.splitext(url_path)[-1]
    return file_ext


def fetch_spacex_launch(launch_id: str):
    launch_url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(launch_url)
    response.raise_for_status()
    response_data = response.json()
    space_x_images_url = response_data['links']['flickr']['original']

    for counter, image_url in enumerate(space_x_images_url):
        image_name = f'spacex_{counter}.jpg'
        download_image(image_url, './images/spacex', image_name)


def download_image(image_url: str, path_to_save: str, image_name: str, params=None):
    response = requests.get(image_url, params=params)
    response.raise_for_status()

    print('DEBUG response_status_code:', response.status_code)
    print('DEBUG response_text:', response.text)

    Path(path_to_save).mkdir(exist_ok=True)
    with open(f'{path_to_save}/{image_name}', 'wb') as image_file:
        image_file.write(response.content)


def main():
    load_dotenv()
    nasa_token = os.environ.get('NASA_TOKEN')
    fetch_spacex_launch('5eb87ce4ffd86e000604b337')
    download_apod_images(nasa_token)
    download_epic_images(nasa_token)


if __name__ == '__main__':
    main()
