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

    def get_user_info(self, user_id):
        """
        Получение информации о пользователе VK.

        Args:
            user_id (int): ID пользователя VK.

        Returns:
            dict: Информация о пользователе VK.
        """
        user_info = self.vk.users.get(user_ids=user_id, fields='bdate, sex, city, status, relation, relation_partner, contacts, games, interests, movies, music, occupation, online, personal, schools, universities, verified')[0]
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

    user_id = 5883760

    # Создание объекта пользователя и получение информации о нем
    user = User(vk_user_session, user_id)
    user_info = user.get_user_info()
    print(f"User Info: {user_info}")

    # Получение топовых фотографий пользователя
    top_photos = user.get_top_photos()
    print(f"Top Photos: {top_photos}")