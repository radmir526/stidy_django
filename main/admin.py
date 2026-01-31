# Здесь регистрируются модели для отображения в админке Django

from django.contrib import admin
from .models import Category, Product


# Регистрируем модель Category в админке
# Используем декоратор вместо admin.site.register
@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin):
        # Поля, которые отображаются в списке категорий
    list_display = ['name', 'slug'] 

    # Автоматическое заполнение поля slug на основе name
    # Удобно, чтобы не вводить ссылки вручную
    prepopulated_fields = {'slug': ('name',)} 

# Регистрируем модель Product в админке
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
        # Поля, отображаемые в списке товаров
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    
        # Фильтры в правой части админки
    list_filter = ['available', 'created', 'updated', 'category']

        # Поля, которые можно редактировать прямо из списка
    list_editable = ['price', 'available'] 

        # Автогенерация slug по названию товара
    prepopulated_fields = {'slug': ('name',)}