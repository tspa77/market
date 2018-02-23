from django.shortcuts import render 
from django.http import HttpResponse 
# импортируем модель для CBV
from django.views import generic 
# импортируем нашу модель
from .models import Product

# Стандартный вью — это обычная питон-функция
def index(request):
    return HttpResponse("This Is iShop")

class IndexView(generic.TemplateView): 
    template_name = 'index.html'
#    context_object_name = 'products' # под каким именем передадутся данные в Темплейт
#    model = Product # название Модели

class ProductListView(generic.ListView): 
    template_name = 'products_list.html' # подключаем наш Темплейт
    context_object_name = 'products' # под каким именем передадутся данные в Темплейт
    model = Product # название Модели


class ProductDetail(generic.DetailView): 
    template_name = 'product_detail.html' 
    model = Product

