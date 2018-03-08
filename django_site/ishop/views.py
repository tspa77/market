from django.shortcuts import render 
from django.http import HttpResponse 
from django.urls import reverse
# импортируем модель для CBV
from django.views import generic 
# импортируем нашу модель
from .models import Product, Category, Order

from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy 
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class SignUpView(generic.CreateView): 
    form_class = UserCreationForm 
    success_url = reverse_lazy('login') 
    template_name = 'signup.html'

# Стандартный вью — это обычная питон-функция
def index(request):
    return HttpResponse("This Is iShop")
    
class IndexView(generic.TemplateView): 
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetail(generic.DetailView): 
    template_name = 'product_detail.html' 
    model = Product

    # метод для добавления дополнительной информации в контекст
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # передаем в словарь контекста список всех категорий 
        context['categories'] = Category.objects.all()
        return context

class OneCategoryView(generic.DetailView): 
    template_name = 'one_category.html' 
    model = Category

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductListView(generic.ListView): 
    template_name = 'products_list.html' 
    context_object_name = 'products' # под каким именем передадутся данные в Темплейт
    model = Product # название Модели
    
    # метод для добавления дополнительной информации в контекст
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # передаем в словарь контекста список всех категорий 
        context['categories'] = Category.objects.all()
        return context

class CategoryListView(generic.ListView): 
    template_name = 'categories_list.html' 
    context_object_name = 'categories'
    model = Category

class ProductCreate(UserPassesTestMixin, generic.CreateView): 
    model = Product 
    # название нашего шаблона с формой
    template_name = 'product_new.html' 
    # какие поля будут в форме 
    fields = '__all__'
    
    # проверяем условие, если пользователь — админ, то вернет True и пустит пользователя
    def test_func(self): 
        return self.request.user.is_superuser

class ProductUpdate(UserPassesTestMixin, generic.UpdateView): 
    model = Product 
    template_name = 'product_update.html' 
    fields = '__all__'

    def test_func(self): 
        return self.request.user.is_superuser

class ProductDelete(UserPassesTestMixin, generic.DeleteView): 
    model = Product 
    template_name = 'product_delete.html' 
    success_url = '/products/'
    
    def test_func(self): 
        return self.request.user.is_superuser

class OrderFormView(generic.CreateView): 
    model = Order 
    template_name = 'order_form.html' 
    success_url = '/' 
    # выведем только поля, которые нужно заполнить самому человеку
    fields = ['customer_name', 'customer_phone']
    
    def form_valid(self, form):
        # получаем ID из ссылки и передаем в ORM для фильтрации
        product = Product.objects.get(id=self.kwargs['pk']) 
        user = self.request.user
        # передаём в заказ текущего покупателя 
        if self.request.user.is_authenticated:
            form.instance.user = user
        # передаем в поле товара нашей формы отфильтрованный товар
        form.instance.product = product 
        # super — перезагружает форму, нужен для работы
        return super().form_valid(form)