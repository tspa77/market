# стандартный вью для админки
from django.contrib import admin
# модуль Джанго для определения урлов
from django.urls import path
# импортируем наш файл views из products
from ishop import views

# говорим Джанго о том, что хотим отображать наш вью на главной странице
# а строчкой ниже, ссылка на нашу админку, про нее позже
urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'), 
    path('products/', views.ProductListView.as_view(), name='products'),
    path('admin/', admin.site.urls, name='admin'), 
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='detail'),
]


















'''
path('<int:pk>/', views.ProductDetail.as_view(), name='detail'),

pk — primary_key = ID
int — integer = фильтрует только числовые значения

первое это что-то вроде фильтрации, второе поле в модели на которое смотрит Вьюха перед тем как вывести
'''