from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import requests

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

    def write_msg(self, message):
        vk.method('messages.send', {'user_id': self.user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    def age(self, date: str) -> int:
        age = datetime.datetime.now().year - int(date[-4:])
        return age

    def get_user_id(self) -> dict:
        user_info = {}
        response = vk.method('users.get', {'user_id': self.user_id,
                                           'v': 5.131,
                                           'fields': 'first_name, last_name, bdate, sex, city'})
        if response:
            for key, value in response[0].items():
                if key == 'city':
                    user_info[key] = value['id']
                elif key == 'bdate':
                    user_info['age'] = self.age(value)
                    user_info['bdate'] = value
                else:
                    user_info[key] = value
        else:
            self.write_msg('Ошибка')
        return user_info

    def check_missing_info(self, user_info: dict):
        # Записывает в словрь отсутствующую информацию
        info_missing = []
        for item in ['bdate', 'sex', 'city']:
            if not user_info.get(item):
                info_missing.append(item)
            if user_info.get('bdate'):
                if len(user_info['bdate'].split('.')) != 3:
                    info_missing.append('bdate')
        return info_missing

    def det_addinfo(self, field):
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
            return city_id
        else:
            self.write_msg('неверно указан город')
            return False

    def find_part(self,):
        response = vk2.method('users.search', {
            'age_from': self.user_info['age'] - 3,
            'age_to': self.user_info['age'] + 3,
            'sex': 3 - self.user_info['sex'],
            'city': self.user_info['city'],
            'statis': 1 or 6,
            'has_photo': 1,
            'count': 1000,
            'sort': 0,
            'v': 5.131
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
        return f'{name} {surname}, ссылка на странницу: {url}'

    def photo_get(self, number):
        id_ = self.parts[number]['id']
        response = vk2.method('photos.get', {
            'owner_id': id_,
            'count': 25,
            'album_id': 'profile',
            'rev': 1
        })
        c = 0
        for info in list(response.values())[1]:
                if c > 2:
                    break
                ids = print(info['id'])
                # photo = requests.get(info['sizes'][-1]['url'])
                # print(info['sizes'][-1]['url'])
                c += 1
                vk.method('messages.send', {'user_id': self.user_id, 'attachment': f'photo{id_}_{ids}', 'random_id': randrange(10 ** 7)})


