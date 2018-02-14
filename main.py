import requests
import datetime
from settings import bot_token


def get_bot_updates():
    # получаем ответ от АПИ
    api_response = requests.get(bot_token + 'getUpdates')
    # превращаем в JSON объект
    json_response = api_response.json()
    # берем и возвращаем ключ ["result"]  как результат работы функции
    return json_response["result"]

result = get_bot_updates()

print('У вас {} сообщений'.format(len(result)))
answer = input("Хотите прочесть(y/n)")

if answer == 'y':
    for mess in result:
        ch_name = mess['message']['from']['first_name']
        ch_date = datetime.datetime.fromtimestamp(mess['message']['date']).strftime('%b. %d, %I:%M')
        ch_text = mess['message']['text']
        print('{}, {}:  {}'.format(ch_date, ch_name, ch_text))

print('Сеанс окончен')