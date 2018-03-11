bot_url = "https://api.telegram.org/bot"
exchange_url = "https://test-my-shop.herokuapp.com/api/"

bot_answer = {
'/start': '''Вот какие команды я знаю: \n
/stat - показываю статистику по магазину \n
/products - показываю все товары магазина \n
/categories - показываю категории товаров \n
/orders - показываю заказы \n
/users - показываю пользователей \n
''',
'unrecognized': '{}, Добро пожаловать в мой магазин.'
'\nНапиши /start и я расскажу тебе, что я умею',
}

catalog = {
'/products': ['products/?format=json',[],'товаров'],
'/categories': ['categories/?format=json',[],'категории'],
'/orders': ['orders/?format=json',[],'заказов'],
'/users': ['users/?format=json',[],'пользователей'],
}