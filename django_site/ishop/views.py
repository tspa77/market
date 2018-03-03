from django.shortcuts import render 
from django.http import HttpResponse 
from django.urls import reverse
# импортируем модель для CBV
from django.views import generic 
# импортируем нашу модель
from .models import Product
from .models import Category
from .models import Order


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

class ProductCreate(generic.CreateView): 
    model = Product 
    # название нашего шаблона с формой
    template_name = 'product_new.html' 
    # какие поля будут в форме 
    fields = '__all__'

class ProductUpdate(generic.UpdateView): 
    model = Product 
    template_name = 'product_update.html' 
    fields = '__all__'

class ProductDelete(generic.DeleteView): 
    model = Product 
    template_name = 'product_delete.html' 
    success_url = '/products/'

    #def get_success_url(self, **kwargs):
    #    return reverse('one_category', product.category.id)

class OrderFormView(generic.CreateView): 
    model = Order 
    template_name = 'order_form.html' 
    success_url = '/' 
    # выведем только поля, которые нужно заполнить самому человеку
    fields = ['customer_name', 'customer_phone']

    def form_valid(self, form):
        # получаем ID из ссылки и передаем в ORM для фильтрации
        product = Product.objects.get(id=self.kwargs['pk']) 
        # передаем в поле товара нашей формы отфильтрованный товар
        form.instance.product = product 
        # super — перезагружает форму, нужен для работы
        return super().form_valid(form)