import json
from random import randrange
from pprint import pprint
from pathlib import Path

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import create_tables, drop_tables
from vk_interaction import User, VKSession


def get_env_variable(variable_name):
    """
    Получение значения переменной окружения из файла .env.

    Args:
        variable_name (str): Название переменной окружения.

    Returns:
        str: Значение переменной окружения.
    
    Raises:
        ValueError: Если переменная окружения не найдена.
    """
    env_path = Path('.').joinpath('.env')
    env_text = Path(env_path).read_text()

    for line in env_text.splitlines():
        if line.startswith(variable_name):
            return line.split('=')[1].strip()
    
    raise ValueError(f"{variable_name} не задан в переменных окружения")

class VKBot:
    def __init__(self, vk_session, group_id):
        self.vk_session = vk_session
        self.vk = vk_session.get_api()
        self.longpoll = VkBotLongPoll(vk_session, group_id=group_id)
        self.callback_types = ('show_snackbar', 'open_link', 'open_app')
        
    def send_message(self, user_id, message, keyboard=None, attachment=None):
        self.vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message=message,
            keyboard=keyboard.get_keyboard() if keyboard else None,
            attachment=attachment
        )
    
    def handle_new_message(self, event):
        request = event.object.message['text']
        user_id = event.object.message['from_id']
        
        if request == "Начать":
            keyboard = VkKeyboard()
            keyboard.add_button("Кнопка 1", color=VkKeyboardColor.SECONDARY)
            keyboard.add_button("Кнопка 2", color=VkKeyboardColor.SECONDARY)
            self.send_message(user_id, "Приветственное сообщение", keyboard)
        elif request == "Кнопка 1":
            self.send_profile(user_id)
        elif request == "Кнопка 2":
            self.send_favorites(user_id)
    
    def send_profile(self, user_id):
        msg = 'Красотка Красивая'
        link = 'https://vk.com/titronius'
        attachment = "photo12908812_457240175,photo12908812_457240168"
        
        keyboard = VkKeyboard(inline=True)
        keyboard.add_openlink_button(label='🔗 Ссылка на профиль', link=link)
        keyboard.add_line()
        keyboard.add_callback_button(label='❤️ Добавить в избранное', color=VkKeyboardColor.SECONDARY, payload={"type": "add_to_favorite"})
        keyboard.add_callback_button(label='❌ Добавить в чс', color=VkKeyboardColor.SECONDARY, payload={"type": "add_to_blacklist"})
        keyboard.add_line()
        keyboard.add_callback_button(label='➡️ Следующий', color=VkKeyboardColor.SECONDARY, payload={"type": "next_people"})
        
        self.send_message(user_id, msg, keyboard, attachment)

    def send_favorites(self, user_id):
        # Логика вывода списка избранных людей.
        pass

    def handle_message_edit(self, event):
        if event.object.payload.get('type') in self.callback_types:
            self.vk.messages.sendMessageEventAnswer(
                event_id=event.object.event_id,
                user_id=event.object.user_id,
                peer_id=event.object.peer_id,
                event_data=json.dumps(event.object.payload)
            )
        else:
            print('Unknown callback type')

    def listen(self):
        for event in self.longpoll.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message['text'] != "":
                    self.handle_new_message(event)
            elif event.type == VkBotEventType.MESSAGE_EDIT:
                self.handle_message_edit(event)

if __name__ == "__main__":
    # Загрузка переменных окружения из файла .env
    load_dotenv(dotenv_path=Path('.').joinpath('.env'))

    # Инициализация сессий VK API для группы и пользователя
    vk_group_session = VKSession('VK_GROUP_TOKEN')
    vk_user_session = VKSession('VK_USER_TOKEN')

    # Подключение к базе данных
    db_uri = get_env_variable('DB_URI')
    engine = create_engine(db_uri)
    create_tables(engine)  # Создание таблиц, если их нет

    # Пример использования VKSession и User классов
    user_id = 331709599

    user = User(vk_user_session, user_id)
    user_info = user.get_user_info()
    print(f"User Info: {user_info}")

    top_photos = user.get_top_photos()
    print(f"Top Photos: {top_photos}")

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



    Session = sessionmaker(bind=engine)
    session = Session()

    # Инициализация бота и запуск обработки событий
    group_id = int(get_env_variable('GROUP_ID'))
    bot = VKBot(vk_group_session.vk_session, group_id=group_id)
    bot.listen()

    session.close()