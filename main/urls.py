from django.urls import path
from . import views


# app_name используется для namespace в шаблонах
# Например: {% url 'main:product_list' %}
app_name = 'main'


# Список маршрутов приложения main
urlpatterns = [
    # Главная страница сайта
    # URL: /
    # Вызывает функцию product_list из views.py
    path('', views.product_list, name='product_list'),

    # Список товаров по категории
    # URL: /electronics/ или /books/
    # category_slug передаётся в product_list как аргумент
    path('<slug:category_slug>/', views.product_list, 
         name='product_list_by_category'),

     # Детальная страница товара
    # URL: /12/smartphone-samsung/
    # id и slug передаются в product_detail
    path('<int:id>/<slug:slug>', views.product_detail,
         name='product_detail'),
]