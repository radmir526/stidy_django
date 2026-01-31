from django.db import models
from django.urls import reverse

# Здесь описываются модели базы данных.
# Каждый класс = таблица в БД

class Category(models.Model): 

    # Название категории
    # db_index=True ускоряет поиск и сортировку по этому полю
    name = models.CharField(max_length=100, db_index=True) 

    # slug используется в URL
    # unique=True гарантирует уникальность ссылок
    slug = models.SlugField(max_length=100, unique=True) 

    class Meta:

        # Сортировка категорий по имени по умолчанию
        ordering = ('name',)

        # Названия для отображения в админке
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории' 

    def __str__(self): 
        # Определяет, как объект будет отображаться в админке
        return self.name
    
    def get_absolute_url(self):
        # Возвращает URL страницы с товарами этой категории
        # reverse ищет путь по имени URL, а не по строке
        return reverse('main:product_list_by_category', args=[self.slug])


class Product(models.Model): 
     # Связь "многие к одному" с категорией
    # related_name позволяет обращаться:
    # category.products.all()
    category = models.ForeignKey(Category, related_name='products', 
                                 on_delete=models.CASCADE)
    
    # Название товара
    name = models.CharField(max_length=100, db_index=True) 

        # slug используется в URL страницы товара
    slug = models.SlugField(max_length=100, unique=True) 

     # Изображение товара
    # upload_to формирует структуру папок по дате загрузки
    # blank=True позволяет не загружать изображение
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True) 

        # Описание товара
    description = models.TextField(blank=True)

        # Цена
    # DecimalField используется для денег, а не float
    price = models.DecimalField(max_digits=10, decimal_places=2) 

        # Флаг доступности товара
    available = models.BooleanField(default=True)

        # Дата создания объекта (заполняется автоматически)
    created = models.DateTimeField(auto_now_add=True)  

    # Дата последнего обновления объекта
    updated = models.DateTimeField(auto_now=True) 


    class Meta:
        # Сортировка товаров по имени
        ordering = ('name',)

    def __str__(self):
        # Отображение товара в админке
        return self.name
    
    def get_absolute_url(self):
         # Возвращает URL детальной страницы товара
        # Используется в шаблонах вместо хардкода ссылок
        return reverse("main:product_detail", args=[self.id, self.slug])
    