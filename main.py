import requests
import time
import random
import datetime
from token_key import bot_token
from settings import *

# вспомогательные процедуры

# запрашиваем свежие курсы на криптонаторе
def get_coins_rate():
    # проверяем, свежесть данных, если прошло меньше 1,5 минут то не обновляемся
    # мы же не трейдеры, чё нам драконить API и бота но зато забираю сразу все 4
    # пары. Т.е. кэширую данные.  
    # # Нормальный подход или так не принято?
    if time.time() - coins_rate['timestamp'] < 90:
        return coins_rate
    # получаем ответ от АПИ
    api_response = requests.get(exchange_url + 'btc-usd')
    # превращаем в JSON объект
    json_response = api_response.json()
    # закидываем в словарь
    coins_rate['btc-usd'] = json_response
    # всё тоже для остальных пар. Криптанатор по каждой паре отдельную ссылку даёт
    api_response = requests.get(exchange_url + 'eth-usd')
    json_response = api_response.json()
    coins_rate['eth-usd'] = json_response
    api_response = requests.get(exchange_url + 'btc-rur')
    json_response = api_response.json()
    coins_rate['btc-rub'] = json_response
    api_response = requests.get(exchange_url + 'eth-rur')
    json_response = api_response.json()
    coins_rate['eth-rub'] = json_response
    # временная отметка получения данных
    coins_rate['timestamp'] = time.time() 
    # отладочный принт в консоль
    print("\nSystem Message - Обновили цены\n")
    return coins_rate

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


# Самый Главный Модуль
def main_module():
    newoffset = None
    while True:
        # получаем обновления от бота
        results = get_bot_updates(newoffset)
        for result in results: 
        # если есть что-то новое, то работаем дальше. Если нет - в конец вайла.
            # берем контакты и данные из апдейта
            last_update_id = result['update_id']
            last_chat_id = result['message']['chat']['id']
            last_chat_name = result['message']['chat']['first_name']
            last_msg_date = datetime.datetime.fromtimestamp(result['message']['date']).strftime('%b. %d, %H:%M')

            # Отлавливаем всякие смайлы и репосты, где нет текста
            # и делаем костыль - добавляем капельку текста
            try:
                last_chat_text = result['message']['text']
            except KeyError:
                last_chat_text = ' '
            
            # реакция на сообщение
            if last_chat_text == '/start':
                answer_text = starttext
            elif last_chat_text == '/btcusd':
                coins_rate = get_coins_rate()
                txt = num_format(coins_rate, 'btc-usd')
                answer_text = ('{} $ за 1 биткойн'.format(txt.replace('.', ',')))
            elif last_chat_text == '/ethusd':
                coins_rate = get_coins_rate()
                txt = num_format(coins_rate, 'eth-usd')
                answer_text = ('{} $ за 1 эфир'.format(txt.replace('.', ',')))
            elif last_chat_text == '/btcrub':
                coins_rate = get_coins_rate()
                txt = num_format(coins_rate, 'btc-rub')
                answer_text = ('{} ₽ за 1 биткойн'.format(txt.replace('.', ',')))
            elif last_chat_text == '/ethrub':
                coins_rate = get_coins_rate()
                txt = num_format(coins_rate, 'eth-rub')
                answer_text = ('{} ₽ за 1 эфир'.format(txt.replace('.', ',')))
            elif last_chat_text == '/signal':
                answer_text = ('С вашего счёта списано 100 рублей. Рекомендация:'
                '\n{} в созвездии {}. Ведущие астрологи {} {} {} '
                ''.format(random.choice(planets), random.choice(zodiac), \
                random.choice(act_1), random.choice(act_2), random.choice(coins)))
            else:
                answer_text = (last_chat_name + ', я не понимаю по клингонски.'
                '\nНапиши /start и я расскажу тебе, что я умею')

            # отправляем ответ
            send_answer(last_chat_id, answer_text)

            # дублируем переписку в консоль, надо же знать о чём он там и с кем говорит
            # потом нужно будет научиться в файл писать логи
            now = datetime.datetime.now()
            print('{}  {}: {}'.format(last_msg_date, last_chat_name, last_chat_text))
            print('{}  tuzemun: {}'.format(now.strftime('%b. %d, %H:%M'), answer_text))
            
            # Вопрос-ответ отработаны. Обновляем оффсет, идём на новый заход вайла
            newoffset = last_update_id + 1

# Закончились вспомогательные модули - Стартуем!
# Формируем словарь для пар
coins_rate = {'btc-usd': None, 'eth-usd': None, 'btc-rub': None, 'eth-rub': None, 
'timestamp': 0}

# запрашиваем актальный курс
coins_rate = get_coins_rate() 

if __name__ == '__main__':  
    try:
        main_module()
    except KeyboardInterrupt:
        exit()