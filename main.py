# - Поехали! (с)


import requests

def get_bot_updates():
    url = "https://api.telegram.org/bot538702489:AAEZkKKJyaB-AYimhlxCawQ5ximbH22rIZ0/getUpdates"
    result = requests.get(url)
    pydict = result.json()
    return pydict['result']


result = get_bot_updates()


print('У вас {} сообщений'.format(len(result)))
answer = input("Хотите прочесть(Y/N)")

if answer == 'Y':
    for mess in range(len(result)):
        print(result[mess]['message']['from']['first_name'],': ', result[mess]['message']['text'] )

print('Сеанс окончен')