import requests
import datetime
from token_key import bot_token
from settings import *

# подключение и запрос данных у бота
def get_bot_updates(offset=None, timeout=30):
    params = {'offset': offset, 'timeout': timeout}
    api_response = requests.get(bot_url + bot_token + '/getUpdates', params)
    json_response = api_response.json()
    return json_response["result"]

# получаем json c сайта
def get_shop_json(parametr):
    api_response = requests.get(exchange_url + parametr)
    json_response = api_response.json()
    print(parametr, ' - Получили данные')
    return json_response

# реакция на сообщение, выбор ответа и ответ
def choice_answer(last_chat_text, last_chat_name, last_chat_id):
    # проверяем есть ли текст в словаре 
    if last_chat_text in bot_answer:
        parametr = (bot_answer[last_chat_text])
        # если да - делаем запрос
        results_site = get_shop_json(parametr)
        quantity = len(results_site)
        answer_text = ('В базе {} товаров').format(quantity)
        for result_site in results_site:
            # работа с текстом
            product_id = result_site['id']
            title = result_site['title']
            answer_text += ('\n ID {}: {}').format(product_id, title)
            
            

    # если нет
    else:
        answer_text = (bot_answer['unrecognized']).format(last_chat_name)
    # отправляем ответ
    
    send_answer(last_chat_id, answer_text)
    # дублируем в консоль
    now = datetime.datetime.now()
    print('{}  tuzemun: {}'.format(now.strftime('%b. %d, %H:%M:%S'), answer_text))

# отправка ответа от бота
def send_answer(chat_id, answer_text):
    params = {'chat_id': chat_id, 'text': answer_text}
    response = requests.post(bot_url + bot_token + '/sendMessage', params)
    return response

def main_module():
    newoffset = None
    print('      *** Перехожу в режим ожидания       ***')
    while True:
        results = get_bot_updates(newoffset)
        for result in results: 
            # проверка на редактированое сообщение. лог и выход из цикла если да
            if 'edited_message' in result:
                continue

            # работа с текстом
            last_update_id = result['update_id']
            last_chat_id = result['message']['chat']['id']
            last_chat_name = result['message']['chat']['first_name']
            last_msg_date = datetime.datetime.fromtimestamp(\
            result['message']['date']).strftime('%b. %d, %H:%M:%S')
            
            # Отлавливаем всякие смайлы и репосты, где нет текста
            try:
                last_chat_text = result['message']['text']
            except KeyError:
                last_chat_text = ' '
            
            # дублируем запрос в консоль, надо же знать кто и что его спрашивает
            print('{}  {}: {}'.format(last_msg_date, last_chat_name, last_chat_text))

            # реакция на сообщение, выбор ответа и сразу ответ
            choice_answer(last_chat_text, last_chat_name, last_chat_id)
            
            # Вопрос-ответ отработаны. Обновляем оффсет, идём на новый заход вайла
            newoffset = last_update_id + 1


# Закончились вспомогательные модули - Стартуем!
print('Поехали! (с)  \n')

if __name__ == '__main__':  
    try:
        main_module()
    except KeyboardInterrupt:
        exit()