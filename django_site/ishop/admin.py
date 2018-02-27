# импортируем из джанго методы добавления в админку
from django.contrib import admin 
# импортируем нашу модель
from .models import Product
from .models import Category


# говорим админке зарегисрировать нашу модель
admin.site.register(Product)
admin.site.register(Category)