# Тут мы регистрируем наши модели для админки

from django.contrib import admin
from .models import Category, Product

@admin.register(Category) # ТУт мы с помощью декоратора регестрируем наш класс модели Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug'] # это те параметры, которые мы будем видеть в админке
    prepopulated_fields = {'slug': ('name',)} # добавили автоматическое заполнение слагов, то есть ссылка будет генериться опираясь на название продукта


@admin.register(Product) # так же регестрируем класс Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    
    list_filter = ['available', 'created', 'updated', 'category'] # это то, по каким параметрам можно будет фильтровать в админке
    list_editable = ['price', 'available'] # параметры, которые можно изменять
    prepopulated_fields = {'slug': ('name',)}