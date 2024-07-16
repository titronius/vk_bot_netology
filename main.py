import random
from datetime import datetime

import settings
from models import User, Relationship, BdInstruments
from vk_interection import VKSession,VkUser
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


vk_session = vk_api.VkApi(token = settings.group_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id= settings.group_id)

vk_group_session = VKSession(settings.group_token)
vk_user_session = VKSession(settings.user_token)

# функции
def get_profiles(vk_id, status_id):
    """
    Получение профилей пользователей для различных статусов.
    """
    user_bd = User.user_check(vk_id)
    user_to_show_id = Relationship.get_users(user_bd.id, status_id)
    if not user_to_show_id and status_id not in [3,4]:
        user = VkUser(vk_group_session, vk_id)
        user_info = user.get_user_info()
        try:
            birthdate = datetime.strptime(user_info['bdate'], "%d.%m.%Y")
            age = datetime.now().year - birthdate.year - ((datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))
        except:
            age = random.randint(18, 45)

        search_params = {
            'sex': 1 if user_info['sex'] == 2 else 2,
            'city': user_info['city']['id'],
            'age': age
        }
        
        user_ids = vk_user_session.search_users(search_params)
        msg = f"💿 Подбираем подходящих пользователей..."
        vk.messages.send(user_id = vk_id, random_id = get_random_id(), message = msg)
        
        for user_id in user_ids:
            check_user = User.user_check(user_id)
            if not check_user:
                related_id = User.user_add(user_id)
                Relationship.relationship_add(user_bd.id, related_id, 1)
        
        msg = f"Найдено {len(user_ids)} пользователей"
        vk.messages.send(user_id = vk_id, random_id = get_random_id(), message = msg)
        user_to_show_id = Relationship.get_users(user_bd.id, 1)
    return user_to_show_id

def send_profile(vk_id, profile_id):
    """
    Отправка профиля пользователя с инофрмацией и с кнопками действия.
    """
    profile_vk_id = User.user_get(profile_id).vk_id
    profile = VkUser(vk_user_session, profile_vk_id)
    profile_info = profile.get_user_info()
    if profile_info['is_closed']:
        Relationship.status_set(vk_id, profile_id, 2)
        user_to_show_id = get_profiles(vk_id, 1)
        send_profile(vk_id, user_to_show_id)
    else:
        msg = f"{profile_info['first_name']} {profile_info['last_name']}"
        link = f'https://vk.com/id{profile_vk_id}'
        attachment = ','.join(profile.get_top_photos())

        keyboard = VkKeyboard(inline = True)
        keyboard.add_openlink_button(label = '🔗 Ссылка на профиль', link = link)
        keyboard.add_line()
        keyboard.add_callback_button(label = '❤️ Добавить в избранное', color=VkKeyboardColor.SECONDARY, payload = {"type": f"add_to_favorite:{profile_id}"})
        keyboard.add_line()
        keyboard.add_callback_button(label = '❌ Добавить в чс', color=VkKeyboardColor.SECONDARY, payload = {f"type": f"add_to_blacklist:{profile_id}"})
        keyboard.add_line()
        keyboard.add_callback_button(label = '➡️ Следующий', color=VkKeyboardColor.SECONDARY, payload = {f"type": f"next_people:{profile_id}"})
        
        vk.messages.send(user_id = vk_id, random_id = get_random_id(), keyboard = keyboard.get_keyboard(), message = msg, attachment = attachment)

def get_list_of_users(vk_id, users, status_id):
    """
    Отправка списков пользователей, в частности избранных.
    """
    if status_id == 3:
        msg = '😍 Список крашей 😍\n\n'
    i = 1
    for user in users:
        profile = VkUser(vk_user_session, user)
        profile_info = profile.get_user_info()
        msg += f"{i}. {profile_info['first_name']} {profile_info['last_name']}\nСсылка: https://vk.com/id{user}\n\n"
        i += 1
    vk.messages.send(user_id = vk_id, random_id = get_random_id(), message = msg, dont_parse_link = 0)

def check_user(vk_id):
    """
    Проверка и добавление юзера в бд.
    """
    check_user = User.user_check(vk_id)
    if not check_user:
        User.user_add(vk_id)

if __name__ == '__main__':
    #Обработчки сообщений
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            # текстовые
            if event.object.message['text'] != "":
                request = event.object.message['text']

                if request == "Начать":
                    check_user(event.object.message['from_id'])
                    keyboard = VkKeyboard()
                    keyboard.add_button(settings.buttons_for_bot[0], color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button(settings.buttons_for_bot[1], color=VkKeyboardColor.SECONDARY)
                    if event.object.message['from_id'] in settings.admins_id:
                        keyboard.add_line()
                        keyboard.add_button(settings.admins_buttons[0], color=VkKeyboardColor.SECONDARY)
                        keyboard.add_button(settings.admins_buttons[1], color=VkKeyboardColor.SECONDARY)
                        keyboard.add_line()
                        keyboard.add_button(settings.admins_buttons[2], color=VkKeyboardColor.SECONDARY)

                    vk.messages.send(user_id = event.object.message['from_id'], random_id = get_random_id(), keyboard = keyboard.get_keyboard(), message = settings.greeting_msg)
                
                elif request == settings.buttons_for_bot[0]:
                    user_to_show_id = get_profiles(event.object.message['from_id'], 1)
                    send_profile(event.object.message['from_id'], user_to_show_id)
    
                elif request == settings.buttons_for_bot[1]:
                    users = get_profiles(event.object.message['from_id'], 3)
                    if users:
                        get_list_of_users(event.object.message['from_id'], users, 3)
                    else:
                        vk.messages.send(user_id = event.object.message['from_id'], random_id = get_random_id(), message = '💔 Избранных пока нет')
                    

                elif event.object.message['from_id'] in settings.admins_id:
                    if request == settings.admins_buttons[0]:
                        BdInstruments.create_tables()
                        vk.messages.send(user_id = event.object.message['from_id'], random_id = get_random_id(), message = "✅ Таблицы в бд созданы")
                    elif request == settings.admins_buttons[1]:
                        BdInstruments.drop_tables()
                        vk.messages.send(user_id = event.object.message['from_id'], random_id = get_random_id(), message = "✅ Таблицы в бд удалены")
                    elif request == settings.admins_buttons[2]:
                        BdInstruments.data_add()
                        vk.messages.send(user_id = event.object.message['from_id'], random_id = get_random_id(), message = "✅ Статусы добавлены")
                else:
                    vk.messages.send(user_id = event.object.message['from_id'], random_id = get_random_id(), message = "Не знаю что ответить на это 🤷‍♂️")

        # ивенты
        elif event.type == VkBotEventType.MESSAGE_EVENT:

            if event.object.payload.get('type') not in settings.CALLBACK_TYPES:
                act, data = event.object.payload.get('type').split(':')
                if act == 'next_people':
                    status_id = 2
                elif act == 'add_to_favorite':
                    status_id = 3
                    vk.messages.send(user_id = event.object['user_id'], random_id = get_random_id(), message = '❤️ Пользователь добавлен в список избранных.\nПоказываем следующего...')
                elif act == 'add_to_blacklist':
                    status_id = 4
                    vk.messages.send(user_id = event.object['user_id'], random_id = get_random_id(), message = '👎🏻 Пользователь добавлен в ЧС.\nПоказываем следующего...')
                Relationship.status_set(event.object['user_id'], data, status_id)
                vk.messages.delete(peer_id = event.object['user_id'], delete_for_all = 1, cmids = event.object['conversation_message_id'])
                user_to_show_id = get_profiles(event.object['user_id'], 1)
                send_profile(event.object['user_id'], user_to_show_id)