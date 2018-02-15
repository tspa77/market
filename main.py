import requests
import datetime
from settings import bot_token

# #################
# процедуры
# #################

# подключение и запрос данных у бота
def get_bot_updates():
    # получаем ответ от АПИ
    api_response = requests.get(bot_token + 'getUpdates')
    # превращаем в JSON объект
    json_response = api_response.json()
    # берем и возвращаем ключ ["result"]  как результат работы функции
    return json_response["result"]

# получение ответа от бота
def send_answer(chat_id, answer_text):
    params = {'chat_id': chat_id, 'text': answer_text}
    respon = requests.post(bot_token + 'sendMessage', params)
    return respon
result = get_bot_updates()

# распечатка полученного массива последних сообщений
def print_result_log():
    for mess in result:
        ch_name = mess['message']['from']['first_name']
        ch_date = datetime.datetime.fromtimestamp(mess['message']['date']).strftime('%b. %d, %H:%M')
        ch_text = mess['message']['text']
        print('{}, {}:  {}'.format(ch_date, ch_name, ch_text))

# #################
# начало работы
# #################

# здороваемся и предлагаем посмотреть переписку
print('\n \nПриветствую тебя, о Повелитель!\nВ моём уютном чатике {} сообщений.'.format(len(result)))
if len(result) > 0:
        answer = input("\nХотите, я Вам прочту (y/n)")
        if answer == 'y':
            print_result_log()

# отклик на сообщение:
# берем контакты последнего кто обращался
last_chat_id = result[-1]['message']['chat']['id']
last_chat_text = result[-1]['message']['text']
last_chat_name = result[-1]['message']['chat']['first_name']

# здороваемся с последним
answer_text = last_chat_name + ', привет!'
send_answer(last_chat_id, answer_text)
