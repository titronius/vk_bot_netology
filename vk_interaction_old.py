import vk_api
from dotenv import load_dotenv
from pathlib import Path


# Загрузка переменных окружения из файла .env
env_path = Path('.').joinpath('.env')
load_dotenv(dotenv_path=env_path)


# Функция для получения сессии API ВКонтакте
def get_vk_session(token_name='VK_GROUP_TOKEN'):
    env_text = Path(env_path).read_text()
    token = None

    for line in env_text.splitlines():
        if line.startswith(token_name):
            token = line.split('=')[1].strip()
            break

    if not token:
        raise ValueError(f"{token_name} не задан в переменных окружения")

    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    return vk


# Получает информацию о пользователе
# vk -сессия API ВКонтакте и user_id - идентификатор пользователя.
def get_user_info(vk, user_id):
    user_info = vk.users.get(user_ids=user_id, fields='bdate,sex,city,status')[0]
    return user_info

# Получает и сортирует фотографии по количеству лайков в порядке убывания
# Возвращает только большие фотографии (type='w')
def get_top_photos(vk, user_id, count=3):
    # owner_id - идентификатор владельца фотографий и extended - получить расширенную информацию
    photos = vk.photos.getAll(owner_id=user_id, extended=1)['items']
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

if __name__ == "__main__":
    # Получаем сессию API с токеном группы для получения информации о пользователе
    vk_group = get_vk_session('VK_GROUP_TOKEN')

    user_id = 5883760
    user_info = get_user_info(vk_group, user_id)
    print(f"User Info: {user_info}")

    # Получаем сессию API с пользовательским токеном для получения фотографий
    vk_user = get_vk_session('VK_USER_TOKEN')

    top_photos = get_top_photos(vk_user, user_id)
    print(f"Top Photos: {top_photos}")