from vk_api.longpoll import VkEventType
import json
from Vkbot import VKbot, longpoll

import json
def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }

keyboard = {
    "one_time": False,
    "buttons": [
        [get_button('Начать поиск', 'primary')],
        [get_button('Вперёд', 'secondary')]
    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


if __name__ == '__main__':
    c = 0
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()
                ids = event.user_id
                user = VKbot(ids)
                if request == "начать поиск":
                    user.write_msg(f"Ищу, {user.user_info['first_name']}")
                    if len(user.check_missing_info()) != 0:
                        for info in user.check_missing_info():
                            user.det_addinfo(info)
                    print(user.get_person(c))
                    user.write_msg(user.get_person(c), user.photo_get(c))
                    c += 1
                elif request == 'вперёд':
                    print(user.get_person(c))
                    user.write_msg(user.get_person(c), user.photo_get(c))
                    c += 1
                elif request == "пока":
                    user.write_msg("Пока((")
                else:
                    user.write_msg("Не понял вашего ответа...")
