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
    path('one_category/<int:pk>/', views.OneCategoryView.as_view(), name='one_category'),
    path('admin/', admin.site.urls, name='megaadmin'), 
]
