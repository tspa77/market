# стандартный вью для админки
from django.contrib import admin
# модуль Джанго для определения урлов
from django.urls import path
# импортируем наш файл views из products
from ishop import views
from django.conf.urls import include

urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'), 
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('products/<int:pk>/order', views.OrderFormView.as_view(), name='product_order'),
    path('products/new/', views.ProductCreate.as_view(), name='product_create'),
    path('products/update/<int:pk>/', views.ProductUpdate.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', views.ProductDelete.as_view(), name='product_delete'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('one_category/<int:pk>/', views.OneCategoryView.as_view(), name='one_category'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('admin/', admin.site.urls,), 
]