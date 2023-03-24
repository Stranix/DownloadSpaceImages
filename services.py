import requests

from pathlib import Path


def download_image(image_url: str, path_to_save: str, image_name: str, params=None):
    print('Загрузка картинке по ссылке:', image_url)
    response = requests.get(image_url, params=params)
    response.raise_for_status()

    print('DEBUG response_status_code:', response.status_code)

    Path(path_to_save).mkdir(exist_ok=True)
    with open(f'{path_to_save}/{image_name}', 'wb') as image_file:
        image_file.write(response.content)

    print('Загрузка завершена')
    print('-' * 25)
