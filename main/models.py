from django.db import models
from django.urls import reverse


# Тут мы прописываем все необходимое для нашей базы данных


class Category(models.Model): # это класс для категорий 
    name = models.CharField(max_length=100, db_index=True) # Создаем поле name, ограничиваем длинну поля и добавляем индекс для сортировки категорий, потому что name всегда будет учавствовать там
    slug = models.SlugField(max_length=100, unique=True) #Слаг нужен для создания ссылок например по называнию продукта https://chernaya-futbolka.com

    class Meta: # это параметры с которыми будет работать база данных и админка
        ordering = ('name',)
        verbose_name = 'Категория' # если мы будем переводить админку на русский язык
        verbose_name_plural = 'Категории' #Множественное число 

    def __str__(self): # этот метод определяет то, как у нас будет отображаться тот или иной объект в админке
        return self.name
    
    def get_absolute_url(self):
        return reverse('main:product_list_by_category', args=[self.slug])


class Product(models.Model): # Прописываем модель нашего продукта
    category = models.ForeignKey(Category, related_name='products', # в эту переменную мы засунули класс Category
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True) # Устанавливаем наименование продукта
    slug = models.SlugField(max_length=100, unique=True) # Устанавливаем ссылки для продуктов
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True) # Добавляем поле с фотографиями, которые будут сохранятся в папки относительно года, месяца и дня загрузки этих фотографий, так же добавили возможность не загружать фото вовсе
    description = models.TextField(blank=True) # устанавливаем описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # устанавливаем прайс с числом с плавающей точкой
    available = models.BooleanField(default=True) # Доступность товаров
    created = models.DateTimeField(auto_now_add=True) # Дата создания будет появляться автоматически 
    updated = models.DateTimeField(auto_now=True) # Дата обновления товара

    class Meta: # класс мета он показывает что будет показываться в админке
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Возвращает URL для страницы с товарами этой категории.
        # Используется в шаблонах для ссылок без хардкода путей. Мы не пишем сами ссылки, а они автоматически подставляются при нажатии на какой либо продукт
        return reverse("main:product_detail", args=[self.id, self.slug])
    