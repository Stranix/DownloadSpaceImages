import os
import requests
import datetime

from dotenv import load_dotenv
from services import download_image


def get_epic_image_urls(api_key: str = 'DEMO_KEY') -> list:
    epic_image_urls = []
    url = 'https://api.nasa.gov/EPIC/api/natural?api_key=DEMO_KEY'
    params = {
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    for image in response.json():
        image_date_time = datetime.datetime.fromisoformat(image['date'])
        image_date = datetime.date.strftime(image_date_time, '%Y/%m/%d')
        image_name = '{}.png'.format(image['image'])
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}'
        epic_image_urls.append(image_url)

    return epic_image_urls


def fetch_epic_images(api_key: str = 'DEMO_KEY'):
    params = {
        'api_key': api_key
    }
    images_url = get_epic_image_urls()
    for counter, url in enumerate(images_url):
        image_name = f'epic_{counter}.png'
        download_image(url, './images/epic', image_name, params)


def main():
    load_dotenv()
    nasa_token = os.environ.get('NASA_TOKEN')

    fetch_epic_images(nasa_token)


if __name__ == '__main__':
    main()
