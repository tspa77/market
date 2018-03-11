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
def get_shop_json(catalog, what):
    if what == "/stat":
        for key in catalog:
            api_response = requests.get(exchange_url + catalog[key][0], auth=('bot', 'shopobot'))
            catalog[key][1] = api_response.json()
    else:
        api_response = requests.get(exchange_url + catalog[what][0], auth=('bot', 'shopobot'))
        catalog[what][1] = api_response.json()
    return catalog

# реакция на сообщение, выбор ответа и ответ
def choice_answer(last_chat_text, last_chat_name, last_chat_id, catalog):
    # проверяем есть ли текст в словаре 
    if last_chat_text == '/stat':
        send_answer(last_chat_id, 'Ожидайте, звоню управляющему.....')
        catalog = get_shop_json(catalog, last_chat_text)
        answer_text = ('На текущий момент в магазине:')
        answer_text += (' \n {} товаров').format(len(catalog['/products'][1]))
        answer_text += (' в {} категориях').format(len(catalog['/categories'][1]))
        answer_text += ('\n {} пользователей').format(len(catalog['/users'][1]))
        answer_text += (' и {} заказов').format(len(catalog['/orders'][1]))

    elif last_chat_text == '/products':
        catalog = get_shop_json(catalog, last_chat_text)
        answer_text = ('На текущий момент в магазине:')
        answer_text += (' \n {} товаров').format(len(catalog[last_chat_text][1]))
        for product in catalog[last_chat_text][1]:
            answer_text += (' \n ID {}:   {}').format(product['id'], product['title'])

    elif last_chat_text == '/categories':
        catalog = get_shop_json(catalog, last_chat_text)
        answer_text = ('На текущий момент в магазине:')
        answer_text += (' \n {} категорий').format(len(catalog[last_chat_text][1]))
        for categories in catalog[last_chat_text][1]:
            answer_text += (' \n ID {}:   {}').format(categories['id'], categories['title'])

    elif last_chat_text == '/orders':
        catalog = get_shop_json(catalog, last_chat_text)
        answer_text = ('На текущий момент в магазине:')
        answer_text += (' \n {} заказов').format(len(catalog[last_chat_text][1]))
        
        tovar = {}
        for product in catalog['/products'][1]:
            tovar.update({product['id']:product['title']})

        for order in catalog[last_chat_text][1]:
            answer_text += (' \nID {}: \nТовар:   {} \nКлиент:   {} \nТелефон:   {}'
            '').format(order['id'], tovar[order['product']], order['customer_name'], order['customer_phone'])


    elif last_chat_text == '/start':
        answer_text = bot_answer['/start']
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
            choice_answer(last_chat_text, last_chat_name, last_chat_id, catalog)
            
            # Вопрос-ответ отработаны. Обновляем оффсет, идём на новый заход вайла
            newoffset = last_update_id + 1


# Закончились вспомогательные модули - Стартуем!
print('Поехали! (с)  \n')

catalog = get_shop_json(catalog, '/stat')

if __name__ == '__main__':  
    try:
        main_module()
    except KeyboardInterrupt:
        exit()