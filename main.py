import requests
import time
import random
import datetime
from token_key import bot_token
from settings import *

# вспомогательные процедуры

# запрос обновления (или отдаём кэшированные)
def get_coins_rate():
    if time.time() - coins_rate['timestamp'] < 90:
        return coins_rate
    # обновляем все пары по очереди
    for pair in coins_rate:
        coins_to_dict(pair)
    print("\nSystem Message - Обновили цены\n")
    return coins_rate

# обновление всех пар и отметки времени в словаре
def coins_to_dict(pair):
    if pair != 'timestamp':
        # получаем ответ от АПИ
        api_response = requests.get(exchange_url + pair)
        # превращаем в JSON объект
        json_response = api_response.json()
        coins_rate[pair] = json_response
    else:
        coins_rate['timestamp'] = time.time() 

# подключение и запрос данных у бота
def get_bot_updates(offset=None, timeout=30):
    params = {'offset': offset, 'timeout': timeout}
    # получаем ответ от АПИ
    api_response = requests.get(bot_url + bot_token + '/getUpdates', params)
    # превращаем в JSON объект
    json_response = api_response.json()
    # берем и возвращаем ключ ["result"] как результат работы функции
    return json_response["result"]

# отправка ответа от бота
def send_answer(chat_id, answer_text):
    params = {'chat_id': chat_id, 'text': answer_text}
    response = requests.post(bot_url + bot_token + '/sendMessage', params)
    return response

# формируем красивый вид полученного числа
def num_format(coins_rate, pair):
    txt = (float(coins_rate[pair]['ticker']['price'][:-6]))
    txt = '{0:,}'.format(txt).replace(',', ' ')
    return txt

# реакция на сообщение, выбор ответа
def choice_answer(last_chat_text, last_chat_name):
    if last_chat_text in answers_with_request:
        coins_rate = get_coins_rate()
        if last_chat_text == '/btcusd':
            txt = num_format(coins_rate, 'btc-usd')
            answer_text = ('{} $ за 1 биткойн'.format(txt.replace('.', ',')))
        elif last_chat_text == '/ethusd':
            txt = num_format(coins_rate, 'eth-usd')
            answer_text = ('{} $ за 1 эфир'.format(txt.replace('.', ',')))
        elif last_chat_text == '/btcrub':
            txt = num_format(coins_rate, 'btc-rur')
            answer_text = ('{} ₽ за 1 биткойн'.format(txt.replace('.', ',')))
        elif last_chat_text == '/ethrub':
            txt = num_format(coins_rate, 'eth-rur')
            answer_text = ('{} ₽ за 1 эфир'.format(txt.replace('.', ',')))
    elif last_chat_text in answers_wo_request:
        if last_chat_text == '/start':
            answer_text = starttext
        elif last_chat_text == '/signal':
            answer_text = ('С вашего счёта списано 1000 рублей. Рекомендация:'
            '\n{} в созвездии {}. Ведущие астрологи {} {} {} '
            ''.format(random.choice(planets), random.choice(zodiac), \
            random.choice(act_1), random.choice(act_2), random.choice(coins)))
    else:
        answer_text = (last_chat_name + ', я не понимаю по клингонски.'
        '\nНапиши /start и я расскажу тебе, что я умею')
    return answer_text


# Самый Главный Модуль
def main_module():
    newoffset = None
    while True:
        # получаем обновления от бота, если обновлений нет - в конец вайла.
        results = get_bot_updates(newoffset)
        for result in results: 
            # проверка на редактированое сообщение. лог и выход из цикла если да
            if 'edited_message' in result:
                Neo = result['edited_message']['chat']['first_name']
                now = datetime.datetime.now()
                print('{}  *** {} пытался сломать матрицу! ***'
                ''.format(now.strftime('%b. %d, %H:%M:%S'), Neo))
                last_chat_id = result['edited_message']['chat']['id']
                answer_text = ('Ваша запись уже была внесена в блокчейн.'
                ' Исправления невозможны!')
                send_answer(last_chat_id, answer_text)
                newoffset = result['update_id'] + 1
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
            
            # реакция на сообщение, выбор ответа
            answer_text = choice_answer(last_chat_text, last_chat_name)
            
            # отправляем ответ
            send_answer(last_chat_id, answer_text)
            
            # дублируем переписку в консоль, надо же знать о чём он там и с кем говорит
            now = datetime.datetime.now()
            print('{}  {}: {}'.format(last_msg_date, last_chat_name, last_chat_text))
            print('{}  tuzemun: {}'.format(now.strftime('%b. %d, %H:%M:%S'), answer_text))
            
            # Вопрос-ответ отработаны. Обновляем оффсет, идём на новый заход вайла
            newoffset = last_update_id + 1

# Закончились вспомогательные модули - Стартуем!
# Формируем словарь для пар
coins_rate = {'btc-usd': None, 'eth-usd': None, 'btc-rur': None, 'eth-rur': None, 
'timestamp': 0}
# запрашиваем актуальный курс
coins_rate = get_coins_rate() 

if __name__ == '__main__':  
    try:
        main_module()
    except KeyboardInterrupt:
        exit()