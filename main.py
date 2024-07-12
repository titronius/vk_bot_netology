from random import randrange

import settings
import json
# from models import User
from vk_interection import VKSession,VkUser
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
# from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


vk_session = vk_api.VkApi(token = settings.bot_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=226538050)

vk_group_session = VKSession(settings.bot_token)
vk_user_session = VKSession(settings.bot_token)


CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
# функции
def add_user_to_db(vk_id):
    user = VkUser(vk_user_session, vk_id)
    user_info = user.get_user_info()
    print(f"User Info: {user_info}")

#Обработчки сообщений
for event in longpoll.listen():

    if event.type == VkBotEventType.MESSAGE_NEW:
    # check_user = User.check_exist(event.object.message['from_id'])
    # if not check_user:
    # add_user_to_db(event.object.message['from_id'])
        if event.object.message['text'] != "":
            request = event.object.message['text']

            if request == "Начать":
                keyboard = VkKeyboard()
                keyboard.add_button(settings.buttons_for_bot[0], color=VkKeyboardColor.SECONDARY)
                keyboard.add_button(settings.buttons_for_bot[1], color=VkKeyboardColor.SECONDARY)
                vk.messages.send(user_id = event.object.message['from_id'], random_id = get_random_id(), keyboard = keyboard.get_keyboard(), message = settings.greeting_msg)
            
            elif request == settings.buttons_for_bot[0]:
                # - имя и фамилия,
                # - ссылка на профиль,
                # - три фотографии в виде attachment(https://dev.vk.com/method/messages.send).
                msg = 'Красотка Красивая'
                link = 'https://vk.com/titronius'
                attachment = "photo12908812_457240175,photo12908812_457240168"
                
                keyboard = VkKeyboard(inline = True)
                keyboard.add_openlink_button(label = '🔗 Ссылка на профиль', link = link)
                keyboard.add_line()
                keyboard.add_callback_button(label = '❤️ Добавить в избранное', color=VkKeyboardColor.SECONDARY, payload = {"type": "add_to_favorite"})
                keyboard.add_callback_button(label = '❌ Добавить в чс', color=VkKeyboardColor.SECONDARY, payload = {"type": "add_to_blacklist"})
                keyboard.add_line()
                keyboard.add_callback_button(label = '➡️ Следующий', color=VkKeyboardColor.SECONDARY, payload = {"type": "next_people"})
                
                vk.messages.send(user_id = event.object.message['from_id'], random_id = get_random_id(), keyboard = keyboard.get_keyboard(), message = msg, attachment = attachment)

            elif request == settings.buttons_for_bot[1]:
                # Вывести список избранных людей.
                pass


    elif event.type == VkBotEventType.MESSAGE_EDIT:

        if event.object.payload.get('type') in CALLBACK_TYPES:
            # отправляем серверу указания как какую из кнопок обработать. Это заложено в 
            # payload каждой callback-кнопки при ее создании.
            # Но можно сделать иначе: в payload положить свои собственные
            # идентификаторы кнопок, а здесь по ним определить
            # какой запрос надо послать. Реализован первый вариант.
            r = vk.messages.sendMessageEventAnswer(
                        event_id=event.object.event_id,
                        user_id=event.object.user_id,
                        peer_id=event.object.peer_id,                                                   
                        event_data=json.dumps(event.object.payload))
        else:
            print('хуяк')
            