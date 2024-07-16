from datetime import datetime
import vk_api

class VKSession:
    def __init__(self, token):
        """
        Инициализация сессии VK API.

        Args:
            token_name (str): Название переменной окружения, содержащей токен VK API.
        """
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()

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
            top_photos.append(f"photo{photo['owner_id']}_{photo['id']}")

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
        # city_name = params.get('city', '')
        # city_id = self.get_city_id(city_name) if city_name else 0

        search_params = {
            'sex': params.get('sex', 0),
            'city': params.get('city'),
            'relation': params.get('relation', 0),
            'count': 1000,  # Максимальное количество пользователей для поиска
            'age_from': params.get('age'),
            'age_from': params.get('age'),
            'fields': 'bdate, sex, city, relation, personal'
        }

        users_found = self.vk.users.search(**search_params)['items']
        user_ids = [user['id'] for user in users_found]
        return user_ids
    

    def get_users_db_data(self, params):
        """
        Получение данных пользователей VK в формате для базы данных.

        Args:
            params (dict): Словарь с параметрами поиска:
                - sex (int): Пол (1 — женщина, 2 — мужчина, 0 — любой).
                - city (str): Название города.
                - relation (int): Семейное положение пользователя.
                - smoking (int): Отношение к курению (1 — да, 2 — время от времени, 3 — нет).
                - alcohol (int): Отношение к алкоголю (1 — регулярно, 2 — иногда, 3 — никогда).

        Returns:
            list: Список словарей с данными пользователей для базы данных.
        """
        # Получаем список ID пользователей, удовлетворяющих параметрам поиска
        user_ids = self.search_users(params)[:10]

        # Подготовим список для хранения данных пользователей для базы данных
        users_db_data = []

        for user_id in user_ids:
            # Получаем подробную информацию о пользователе
            user_info = self.get_user_info(user_id)

            # Проверяем корректность поля bdate
            bdate_str = user_info.get('bdate', '01.01.1900')
            if bdate_str == '01.01.1900':
                bdate_parsed = datetime.strptime(bdate_str, '%d.%m.%Y').date()
            else:
                try:
                    if '.' in bdate_str:
                        bdate_parsed = datetime.strptime(bdate_str, '%d.%m.%Y').date()
                    else:
                        bdate_parsed = datetime.strptime(bdate_str, '%d.%m').date()
                except (ValueError, TypeError):
                    bdate_parsed = datetime.strptime('01.01.1900', '%d.%m.%Y').date()

            # Формируем словарь с данными пользователя для базы данных
            user_dict = {
                'id': user_info['id'],
                'first_name': user_info['first_name'],
                'last_name': user_info['last_name'],
                'bdate': bdate_parsed,
                'sex': user_info.get('sex', None),
                'city': user_info.get('city', {}).get('title', ''),
                'relation': user_info.get('relation', None),
                'smoking': params.get('smoking', None),
                'alcohol': params.get('alcohol', None)
            }

            users_db_data.append(user_dict)

        return users_db_data


class VkUser:
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