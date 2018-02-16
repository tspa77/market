import requests
import datetime
import time
from settings import bot_token
# now = datetime.datetime.now()

# вспомогательные процедуры
# подключение и запрос данных у бота
def get_bot_updates(offset=None):
    params = {'offset': offset}
    # получаем ответ от АПИ
    api_response = requests.get(bot_token + 'getUpdates', params)
    # превращаем в JSON объект
    json_response = api_response.json()
    # берем и возвращаем ключ ["result"]  как результат работы функции
    return json_response["result"]

# отправка ответа от бота
def send_answer(chat_id, answer_text):
    params = {'chat_id': chat_id, 'text': answer_text}
    respon = requests.post(bot_token + 'sendMessage', params)
    return respon


# Самый Главный Модуль
def main_module():
    newoffset = None
    while True:
        # получаем обновления от бота
        result = get_bot_updates(newoffset)
        if len(result) > 0: # если есть что-то новое, то работаем дальше. Если нет - в конец вайла. Спим и курим.

            # тут будет цикл, ели вдруг больше одного сообщения прилетело. Но пока работаем с одним - посленим. 
            # берем контакты последнего кто обращался
            last_update_id = result[-1]['update_id']
            last_chat_text = result[-1]['message']['text']
            last_chat_id = result[-1]['message']['chat']['id']
            last_chat_name = result[-1]['message']['chat']['first_name']
            
            # реакция на сообщение
            answer_text = last_chat_name + ', ты сказал: ' + last_chat_text + '   '
            send_answer(last_chat_id, answer_text)
            
            # отладочный принт в консоль
            print(newoffset, "  = newoffset = last_update_id   ", last_chat_text)
            # закончили общаться с пользователем. Обновляем оффсет, идём на новый заход вайла
            newoffset = last_update_id + 1

        # солдат спит, служба идёт
        time.sleep(2)
        # отладочный принт в консоль
        print("  Ничё нового нет, переменные не трогаю, сижу, курю, жду апдейтов   ")



if __name__ == '__main__':  
    try:
        main_module()
    except KeyboardInterrupt:
        exit()