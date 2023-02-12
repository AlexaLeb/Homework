from vk_api.longpoll import VkEventType
import json
import Vkbot
from Vkbot import VKbot, longpoll

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
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()
                ids = event.user_id
                user = VKbot(ids)

                if request == "начать поиск":
                    user.write_msg(f"Ищу, {user.user_info['first_name']}")
                    l = len(user.parts)
                    c = 0
                    while c <= 5:
                        print(user.get_person(c))
                        print(user.photo_get(c))
                        user.write_msg(user.get_person(c)[0:])
                        c += 1




                elif request == "пока":
                    user.write_msg("Пока((")
                else:
                    user.write_msg("Не понял вашего ответа...")
