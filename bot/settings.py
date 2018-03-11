bot_url = "https://api.telegram.org/bot"
exchange_url = "https://test-my-shop.herokuapp.com/api/"

bot_answer = {
'/start': '''Вот какие команды я знаю: \n
/products - показываю все товары магазина \n
/categories - показываю категории товаров \n
/orders - показываю заказы \n
/users - показываю пользователей \n
''',
'/products': 'products/?format=json',
'/categories': 'categories/?format=json',
'/orders': 'orders/?format=json',
'/users': 'users/?format=json',
'unrecognized': '{}, Добро пожаловать в мой магазин.'
'\nНапиши /start и я расскажу тебе, что я умею',
}

