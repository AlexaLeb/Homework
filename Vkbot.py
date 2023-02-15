from random import randrange
import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
from model import db_add_user, db_chek_user_exists, db_get_age

with open('tookenofbot.txt', 'r') as file:
    bot_token = file.readline()
with open('usertooken.txt', 'r') as file:
    user_token = file.readline()
vk = vk_api.VkApi(token=bot_token)
vk2 = vk_api.VkApi(token=user_token)
longpoll = VkLongPoll(vk)


class VKbot:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.user_info = self.get_user_id()
        self.parts = self.find_part()
        self.keyboard = self.keyboard()

    def get_button(self, text, color):
        return {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"" + "1" + "\"}",
                "label": f"{text}"
            },
            "color": f"{color}"
        }

    def keyboard(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.get_button('Начать поиск', 'primary')],
                [self.get_button('вперёд', 'secondary')]
            ]
        }

        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        return str(keyboard.decode('utf-8'))

    def write_msg(self, message, attachment=None):
        vk.method('messages.send', {'user_id': self.user_id, 'message': message, 'random_id': randrange(10 ** 7), 'attachment': attachment, 'keyboard': self.keyboard})

    def age(self, user_info) -> int:
        age = datetime.datetime.now().year - int(user_info[-4:])
        return age

    def get_user_id(self) -> dict:
        user_info = {}
        response = vk.method('users.get', {'user_id': self.user_id,
                                           'v': 5.89,
                                           'fields': 'first_name, last_name, bdate, sex, city'})

        if response:
            for key, value in response[0].items():
                if key == 'city':
                    user_info[key] = value['id']
                elif key == 'bdate':
                    if db_chek_user_exists(user_info['id']) is True:
                        print('пропустил шаг с базой данных')
                    else:
                        n = value
                        if len(n) < 5 and db_chek_user_exists(user_info['id']) is False:
                            print('не нашел возраст')
                            g = self.get_addinfo(key)
                            user_info['age'] = self.age(g)
                            user_info['bdate'] = value
                        else:
                            user_info['age'] = self.age(n)
                            user_info['bdate'] = value
                else:
                    user_info[key] = value

        else:
            self.write_msg('Ошибка')
        if db_chek_user_exists(user_info['id']) is False:
            db_add_user(user_info['id'], user_info['age'])
        user_info['ad_to_db'] = 'yes'
        print(user_info)
        return user_info

    def check_missing_info(self):
        # Записывает в словрь отсутствующую информацию
        info_missing = []
        for item in ['bdate', 'sex', 'city']:
            if not self.user_info.get(item):
                info_missing.append(item)
            if self.user_info.get('bdate'):
                if len(self.user_info['bdate'].split('.')) != 3:
                    info_missing.append('bdate')
        return info_missing

    def get_addinfo(self, field):
        di = {
            'bdate': 'вашу дату рождения в формате dd.mm.yyyy',
            'city': 'ваш город'
        }
        self.write_msg(f'''Недостаточно  о вас информации, введите следующие данные: \n{di[field]}''')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if field == 'city':
                        return self.get_city(event.text)
                    elif field == 'bdate':
                        if len(event.text.split('.')) != 3:
                            self.write_msg('неверно указана дата рождения')
                            self.get_addinfo(field)
                        self.write_msg('Данные изменены')
                        return event.text

    def get_city(self, city):
        di = {
            'country_id': 1,
            'q': city,
            'count': 1
        }

        response = vk2.method('database.getCities', values=di)
        if response['items']:
            city_id = response['items'][0]['id']
            self.user_info['city'] = city_id
            self.write_msg('указан город')
            return True
        else:
            self.write_msg('неверно указан город')
            return False

    def find_part(self):
        a = db_get_age(self.user_info['id'])
        response = vk2.method('users.search', {
            'age_from': a - 3,
            'age_to': a + 3,
            'sex': 3 - self.user_info['sex'],
            'city': self.user_info['city'],
            'statis': 1 or 6,
            'has_photo': 1,
            'count': 1000,
            'sort': 0,
            'v': 5.89,
            'is_closed': False,
            'can_access_closed': True
        })

        if response:
            if response.get('items'):
                return response.get('items')
            else:
                self.write_msg('ошибка')
                return False

    def get_person(self, number=1) -> str:
        name = self.parts[number]['first_name']
        surname = self.parts[number]['last_name']
        url = 'vk.com/id' + str(self.parts[number]['id'])
        return f'{name} {surname}, \nссылка на странницу: \n{url}'

    def photo_get(self, number):
        id_ = self.parts[number]['id']
        response = vk2.method('photos.get', {
            'owner_id': id_,
            'count': 25,
            'album_id': 'profile',
            'rev': 1,
            'extended': 1
        })
        result = []
        c = 0
        while c < 2:
            for foto in sorted(response['items'], key=lambda x: x['likes']['count'], reverse=True):
                c += 1
                result.append(f"photo{foto['owner_id']}_{foto['id']}")
                if len(result) == 3:
                    break
        return ','.join(result)
