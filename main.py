from vk_api.longpoll import VkEventType
from Vkbot import VKbot, longpoll
from model import creator




if __name__ == '__main__':
    c = 0
    creator()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            if request == "начать поиск":
                try:
                    user.write_msg(f"Ищу, {user.user_info['first_name']}\n"
                                   f"Повтороное нажание кнопки приведет к сбросу\n"
                                   f"Пожалуйста, нажимайте только кнопку вперед")
                    user.write_msg(user.get_person(c), user.photo_get(c))
                    c += 1
                except NameError:
                    ids = event.user_id
                    user = VKbot(ids)

            elif request == 'вперёд':
                try:
                    user.write_msg(f"Ищу, {user.user_info['first_name']}")
                    user.write_msg(user.get_person(c), user.photo_get(c))
                    c += 1
                except NameError:
                    ids = event.user_id
                    user = VKbot(ids)
            else:
                user.write_msg("Не понял вашего ответа...\nНеужели у вас нет кнопок? \nНаверное, мой автор идиот")
