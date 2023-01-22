from pprint import pprint

import requests


class YaUploader:
    def __init__(self, tooken: str):
        self.token = tooken

    files_url = "https://cloud-api.yandex.net/v1/disk/resources/files"
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def get_upload_link(self, file_path: str) -> dict:
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(self.upload_url, params=params, headers=self.headers)
        jsonify = response.json()
        pprint(jsonify)
        return jsonify


    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        href = self.get_upload_link(file_path).get("href")
        if not href:
            return

        with open(file_path, 'rb') as file:
            response = requests.put(href, data=file)
            if response.status_code == 201:
                print("файл загружен")
                return True
            print("файл не загружен потому что", response.status_code)
            return False


class VkRequester:
    def __init__(self, token: str, id):
        self.token = token
        self.id = id

    def get_request(self,amount=5): #функция делает запрос, находит числовой id в ВК и выдает информациию о аватарках пользователя
        # params = {
        #     "access_token": self.token,
        #     'owner_id': self.id,
        #     "v": '5.131',
        #     'album_id': 'profile',
        #     'extended': '1'
        # }
        resp = requests.get("https://api.vk.com/method/users.get", params={
            "access_token": self.token,
            'user_ids': self.id,
            "v": '5.131',
        }).json()
        for i in  resp['response']:
            ids = i['id']
        response = requests.get("https://api.vk.com/method/photos.get", params={
            "access_token": self.token,
            'owner_id': ids,
            "v": '5.131',
            'album_id': 'profile',
            'extended': '1',
            'count': amount
        }).json()
        return response

    def get_file_name(self, number, amount=None): #находит количество лайков для имя файла с фото
        file = self.get_request(amount)
        for info in file.items():
            body = list(info[1].values())[1]
            for k, v in body[number].items():
                if k == 'likes':
                    for element, likes in v.items():
                        if element == 'count':
                            return str(likes)

    def photo_get(self, number, amount=None): #выдает размер фото и ссылку на него
        file = self.get_request(amount)
        for info in file.items():
            val = list(info[1].values())[1]
            for k, v in val[number].items():
                if k == 'sizes':
                    fotos = v
            lengh = len(fotos)
            foto = fotos[lengh - 1]
            final = list(foto.values())
            return (final[1], final[3])



    def file_create(self,number): #создает файл с фотографией
        p = self.photo_get(number)[1]
        apiphoto = requests.get(p)
        out = open(f'{self.get_file_name(number)}.jpeg', "wb")
        out.write(apiphoto.content)
        out.close()
        return f'{self.get_file_name(number)}.jpeg'

    def counter(self): #считает сколько у пользователя аватарок, чтобы знать, сколько раз нужно запустить код
        file = self.get_request()
        for info in file.items():
            for count in info[1].values():
                return count





if __name__ == '__main__':
    # # Получить токен от пользователя
    tooken = "y0_AgAAAAA2r5qLAAjJIQAAAADV_tzPu-aTxlY5TDida9NxoAabFObV40Y"
    uploader = YaUploader(tooken)
    id_lina = '311750739'
    id_sasha = '408198842'
    ids = 'lina_not_cynical'
    tokenVK = 'vk1.a.DlTR29AK9-veDvvqvGwmu1RRUP8F-E35NVuHpjtxAivDxwbySbpupsUDNio1Drs8nAK-yEE-PE1Ph856jJodugRpML1hWWNqzIBqDO9j7JBVVmOH03cTcoLCH-LQRkkA4Is59tY0JMTZ-FJ0IglixXl8pOPrSlFmous4c_3HSMxTw8KbNV86R6arqxZX1rrw'
    test = VkRequester(tokenVK, ids)
    test2 = test.get_file_name(1)
    pprint(test2)
    pprint(type(test2))

    # for proccess in range(0, test.counter()):
    #     uploader.upload(test.file_create(proccess))

