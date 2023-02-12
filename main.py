from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

with open('tookenofbot.txt', 'r') as file:
    bot_token = file.readline()
with open('usertooken.txt', 'r') as file:
    user_token = file.readline()

vk = vk_api.VkApi(token=bot_token)
vk2 = vk_api.VkApi(token=user_token)
longpoll = VkLongPoll(vk)

class Vkbot:
    def __int__(self, user_id: str):
        self.user_id = user_id
    def write_msg(message):
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


    def get_user_id(user_id):  # создает словарь с информацией о поользователе
        user_info = {}
        response = vk.method('users.get', {'user_id': user_id,
                                          'v': 5.131,
                                          'fields': 'first_name, last_name, bdate, sex, city'})
        if response:
            for key, value in response[0].items():
                if key == 'city':
                    user_info[key] = value['id']
                else:
                    user_info[key] = value
        else:
            write_msg(user_id, 'Ошибка')
            return False
        return user_info


    def check_missing_info(user_info):
        # Записывает в словрь отсутствующую информацию
        info_missing = []
        for item in ['bdate', 'sex', 'city']:
            if not user_info.get(item):
                info_missing.append(item)
            if user_info.get('bdate'):
                if len(user_info['bdate'].split('.')) != 3:
                    info_missing.append('bdate')
        return info_missing


    def det_addinfo(user_id, field):
        di = {
            'bdate': 'вашу дату рождения в формате dd.mm.yyyy',
            'city': 'ваш город'
        }
        write_msg(user_id, f'''Недостаточно  о вас информации, введите следующие данные: \n{di[field]}''')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if field == 'city':
                        return get_city(user_id, event.text)
                    elif field == 'bdate':
                        if len(event.text.split('.')) != 3:
                            write_msg(user_id, 'неверно указана дата рождения')
                        return event.text


    def get_city(user_id, city):
        di = {
            'country_id': 1,
            'q': city,
            'count': 1
        }

        response = vk2.method('database.getCities', values=di)
        if response['items']:
            city_id = response['items'][0]['id']
            return city_id
        else:
            write_msg(user_id, 'неверно указан город')
            return False


    def find_part(user_info):
        response = vk2.method('users.search', {
            'age_from': user_info['age'] - 3,
            'age_to': user_info['age'] + 3,
            'sex': 3 - user_info['sex'],
            'city': user_info['city'],
            'statis': 6,
            'has_photo': 1,
            'count': 1000,
            'sort': 0,
            'v': 5.131
        })

        if response:
            if response.get('items'):
                return response.get('items')
            else:
                write_msg(user_info['id'], 'ошибка')
                return False



if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "привет" or request == "Привет":
                    write_msg(event.user_id, f"Хай, {event.user_id}")
                    write_msg(event.user_id, get_user_id('408198842'))
                    print(get_user_id('408198842'))
                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не понял вашего ответа...")

