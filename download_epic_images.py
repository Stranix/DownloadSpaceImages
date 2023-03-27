import os
import requests
import datetime

from dotenv import load_dotenv
from services import download_image


def get_list_epic_images_url(api_key: str = 'DEMO_KEY') -> list:
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
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}'
        result.append(image_url)

    return result


def fetch_epic_images(api_key: str = 'DEMO_KEY'):
    params = {
        'api_key': api_key
    }
    images_url = get_list_epic_images_url()
    for counter, url in enumerate(images_url):
        image_name = f'epic_{counter}.png'
        download_image(url, './images/epic', image_name, params)


if __name__ == '__main__':
    load_dotenv()
    nasa_token = os.environ.get('NASA_TOKEN')

    fetch_epic_images(nasa_token)
