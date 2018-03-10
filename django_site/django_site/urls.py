# стандартный вью для админки
from django.contrib import admin
# модуль Джанго для определения урлов
from django.urls import path
# импортируем наш файл views из products
from ishop import views
from django.conf.urls import include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [ 
#    path('', views.IndexView.as_view(), name='index'), 
    path('', views.ProductListView.as_view()),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),

    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('one_category/<int:pk>/', views.OneCategoryView.as_view(), name='one_category'),

    path('products/new/', views.ProductCreate.as_view(), name='product_create'),
    path('products/update/<int:pk>/', views.ProductUpdate.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', views.ProductDelete.as_view(), name='product_delete'),

    path('products/<int:pk>/order', views.OrderFormView.as_view(), name='product_order'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('admin/', admin.site.urls,), 
    
    path('api/products/', views.ProductListAPI.as_view(), name='api_products_list'),
    path('api/categories/', views.CategoryListAPI.as_view(), name='api_categories_list'),
    path('api/orders/', views.OrderListAPI.as_view(), name='api_orders_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 