from vk_api.longpoll import VkEventType
from Vkbot import VKbot, longpoll
from model import creator, db_add_to_seen, db_chek_user_seen




if __name__ == '__main__':
    c = 0
    creator()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            ids = event.user_id
            user = VKbot(ids)
            if event.to_me:
                request = event.text.lower()

                if request == "начать поиск":

                    user.write_msg(f"Ищу, {user.user_info['first_name']}")
                    if db_chek_user_seen(user.find_part()[c]['id'], user.user_id) is False:
                        db_add_to_seen(user.find_part()[c]['id'], user.user_id)
                        if user.find_part()[c]['is_closed'] == True and user.find_part()[c]['can_access_closed'] == False:
                            user.write_msg(f'{user.get_person(c)}')
                        else:
                            user.write_msg(user.get_person(c), user.photo_get(c))
                    else:
                        user.write_msg('видел')

                    c += 1


                elif request == 'вперёд':
                    user.write_msg(f"Ищу, {user.user_info['first_name']}")
                    part = user.find_part()
                    if db_chek_user_seen(part[c]['id'], user.user_id) is False:
                        db_add_to_seen(part[c]['id'], user.user_id)
                        if part[c]['is_closed'] == True and part[c]['can_access_closed'] == False:
                            user.write_msg(f'{user.get_person(c)}')
                        else:
                            user.write_msg(user.get_person(c), user.photo_get(c))
                    else:
                        user.write_msg('видел')
                    c += 1

                else:
                    user.write_msg("Не понял вашего ответа...\nНеужели у вас нет кнопок? \nНаверное, мой автор идиот")
