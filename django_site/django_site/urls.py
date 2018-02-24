# стандартный вью для админки
from django.contrib import admin
# модуль Джанго для определения урлов
from django.urls import path
# импортируем наш файл views из products
from ishop import views

urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'), 
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='detail'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('categorys/', views.CategoryListView.as_view(), name='categorys'),
    path('prod_in_cat/<int:pk>/', views.ProdInCatView.as_view(), name='prod_in_cat'),
    path('admin/', admin.site.urls, name='megaadmin'), 
]




'''
path('<int:pk>/', views.ProductDetail.as_view(), name='detail'),

pk — primary_key = ID
int — integer = фильтрует только числовые значения

первое это что-то вроде фильтрации, второе поле в модели на которое смотрит Вьюха перед тем как вывести
'''