
import vk_api
from dotenv import load_dotenv
from pathlib import Path

# Загрузка переменных окружения из файла .env
load_dotenv(dotenv_path=Path('.').joinpath('.env'))

# Функция для получения сессии VK API


def get_user_info(self, user_id):
    """
    Получение информации о пользователе VK.

    Args:
        user_id (int): ID пользователя VK.

    Returns:
        dict: Информация о пользователе VK.
    """
    user_info = self.vk.users.get(user_ids=user_id, fields='bdate,sex,city,status')[0]

    # Преобразование текстового значения статуса в числовое значение
    status_map = {
        '1': 1,  # не женат (не замужем)
        '2': 2,  # встречается
        '3': 3,  # помолвлен(-а)
        '4': 4,  # женат (замужем)
        '5': 5,  # всё сложно
        '6': 6,  # в активном поиске
        '7': 7,  # влюблен(-а)
        '8': 8   # в гражданском браке
    }

    # Получение числового значения статуса
    status_text = user_info.get('status')
    status_number = status_map.get(status_text, None)

    # Добавление числового значения статуса к информации о пользователе
    user_info['status_number'] = status_number

    return user_info


get_user_info('VK_USER_TOKEN', 5883760)