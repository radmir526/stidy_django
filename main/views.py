# Во views мы обрабатываем запросы пользователя
# и формируем ответ (чаще всего HTML-страницу)


from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


# Испол# Используем функции, а не классы,
# потому что логика простая и проект небольшой
def product_list(request, category_slug=None):

    # Получаем все категории из базы данных
    # Нужно, например, для отображения меню категорий
    categories = Category.objects.all()

    # Получаем все товары, которые доступны для отображения
    products = Product.objects.filter(available=True)
    
    # Переменная для текущей выбранной категории
    category = None

    # Если в URL передан slug категории,
    # значит пользователь открыл страницу конкретной категории
    if category_slug: 

        # Пытаемся получить категорию по slug
        # Если не нашли — Django автоматически вернёт 404
        category = get_object_or_404(Category, slug=category_slug) 

        # Фильтруем товары по выбранной категории
        products = products.filter(category=category)

     # render:
    # 1. request — текущий HTTP-запрос
    # 2. путь к HTML-шаблону
    # 3. context — данные, доступные в шаблоне
    return render(request, 'main/product/list.html', 
                  {'category': category,
                   'categories': categories,
                   'products': products})


# Детальная страница конкретного товара
def product_detail(request, id, slug):  

     # Получаем товар по id и slug
    # Если товар не найден или недоступен — 404
    product = get_object_or_404(Product, 
                                id=id, 
                                slug=slug, 
                                available=True)

    # Получаем похожие товары:
    # - из той же категории
    # - доступные
    # - исключаем текущий товар
    # - ограничиваем результат 4 объектами
    related_products = Product.objects.filter(category=product.category, 
                                              available=True
                                              ).exclude(id=product.id)[:4] 
    
    # Форма добавления товара в корзину
    # Передаётся в шаблон
    cart_product_form = CartAddProductForm()

     # Возвращаем HTML-страницу товара
    return render(request, 'main/product/detail.html', {'product': product,
                                                        'related_products': related_products,
                                                        'cart_product_form': cart_product_form})