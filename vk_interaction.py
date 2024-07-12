from pprint import pprint
from sqlalchemy import create_engine, Column, Integer, String, Date, SmallInteger, ForeignKey, UniqueConstraint, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import vk_api
from dotenv import load_dotenv
from pathlib import Path

class VKSession:
    def __init__(self, token_name):
        """
        Инициализация сессии VK API.

        Args:
            token_name (str): Название переменной окружения, содержащей токен VK API.
        """
        self.token = self._get_token(token_name)
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
    
    def _get_token(self, token_name):
        """
        Получение токена из переменных окружения.

        Args:
            token_name (str): Название переменной окружения, содержащей токен VK API.

        Returns:
            str: Токен VK API.
        
        Raises:
            ValueError: Если токен не найден в переменных окружения.
        """
        env_path = Path('.').joinpath('.env')
        env_text = Path(env_path).read_text()

        for line in env_text.splitlines():
            if line.startswith(token_name):
                return line.split('=')[1].strip()
        
        raise ValueError(f"{token_name} не задан в переменных окружения")
    

    def get_city_id(self, city_name, country_id=1):
        """
        Получение ID города по его названию.

        Args:
            city_name (str): Название города.
            country_id (int, optional): ID страны. По умолчанию 1 (Россия).

        Returns:
            int: ID города.
        
        Raises:
            ValueError: Если город не найден.
        """
        cities = self.vk.database.getCities(country_id=country_id, q=city_name, need_all=1, count=1)['items']
        if not cities:
            raise ValueError(f"Город {city_name} не найден")
        return cities[0]['id']

    def get_user_info(self, user_id):
        """
        Получение информации о пользователе VK.

        Args:
            user_id (int): ID пользователя VK.

        Returns:
            dict: Информация о пользователе VK.
        """
        user_info = self.vk.users.get(user_ids=user_id, fields='bdate, sex, city, status, relation, contacts, games, interests, movies, music, occupation, online, personal, schools, universities, verified')[0]
        return user_info
    
    def get_top_photos(self, user_id, count=3):
        """
        Получение топовых фотографий пользователя VK.

        Args:
            user_id (int): ID пользователя VK.
            count (int, optional): Количество топовых фотографий для получения. По умолчанию 3.

        Returns:
            list: Список URL топовых фотографий.
        """
        photos = self.vk.photos.getAll(owner_id=user_id, extended=1)['items']
        sorted_photos = sorted(photos, key=lambda x: x['likes']['count'], reverse=True)

        top_photos = []
        for photo in sorted_photos:
            sizes = photo['sizes']
            largest_photo = next((size for size in sizes if size['type'] == 'w'), None)
            if largest_photo:
                top_photos.append(largest_photo['url'])

            if len(top_photos) >= count:
                break

        return top_photos
    
    def search_users(self, params):
        """
        Поиск пользователей VK по заданным параметрам.

        Args:
            params (dict): Словарь с параметрами поиска:
                - sex (int): Пол (1 — женщина, 2 — мужчина, 0 — любой).
                - city (str): Название города.
                - relation (int): Семейное положение пользователя.
                - smoking (int): Отношение к курению (1 — да, 2 — время от времени, 3 — нет).
                - alcohol (int): Отношение к алкоголю (1 — регулярно, 2 — иногда, 3 — никогда).

        Returns:
            list: Список ID пользователей, удовлетворяющих заданным параметрам.
        """
        city_name = params.get('city', '')
        city_id = self.get_city_id(city_name) if city_name else 0

        search_params = {
            'sex': params.get('sex', 0),
            'city': city_id,
            'relation': params.get('relation', 0),
            'count': 1000,  # Максимальное количество пользователей для поиска
            'fields': 'bdate, sex, city, relation, personal'
        }
        print(search_params)
        users_found = self.vk.users.search(**search_params)['items']
        user_ids = [user for user in users_found]
        return user_ids


class User:
    def __init__(self, vk_user_session, user_id):
        """
        Инициализация объекта пользователя VK.

        Args:
            vk_user_session (VKSession): Объект сессии VK API для пользователя.
            user_id (int): ID пользователя VK.
        """
        self.vk_user_session = vk_user_session
        self.user_id = user_id
    
    def get_user_info(self):
        """
        Получение информации о пользователе VK.

        Returns:
            dict: Информация о пользователе VK.
        """
        return self.vk_user_session.get_user_info(self.user_id)
    
    def get_top_photos(self, count=3):
        """
        Получение топовых фотографий пользователя VK.

        Args:
            count (int, optional): Количество топовых фотографий для получения. По умолчанию 3.

        Returns:
            list: Список URL топовых фотографий.
        """
        return self.vk_user_session.get_top_photos(self.user_id, count)


if __name__ == "__main__":
    # Загрузка переменных окружения из файла .env
    load_dotenv(dotenv_path=Path('.').joinpath('.env'))

    # Инициализация сессий VK API для группы и пользователя
    vk_group_session = VKSession('VK_GROUP_TOKEN')
    vk_user_session = VKSession('VK_USER_TOKEN')

    user_id = 331709599

    # Создание объекта пользователя и получение информации о нем
    user = User(vk_user_session, user_id)
    user_info = user.get_user_info()
    print(f"User Info: {user_info}")

    # Получение топовых фотографий пользователя
    top_photos = user.get_top_photos()
    print(f"Top Photos: {top_photos}")

    # Поиск пользователей по заданным параметрам
    search_params = {
        'sex': 1,
        'city': 'Оренбург',
        'relation': 6,
        'smoking': 0,
        'alcohol': 0
    }

    user_ids = vk_user_session.search_users(search_params)
    print(f"Найдено пользователей: {len(user_ids)}")
    pprint(f"ID пользователей: {user_ids}")