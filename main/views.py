# во views мы обрабатываем запросы пользователя и отправляем ему соответствующие ответы
# так же добавляем представления для шаблонов


from django.shortcuts import render, get_object_or_404
from .models import Category, Product



# Используем функции, потому что сайт не большой, а если было бы большое количество инфы, то использовали бы классы
def product_list(request, category_slug=None):
    categories = Category.objects.all() # Это параметр который будет выводить все наши категории
    products = Product.objects.filter(available=True)

    category = None
    if category_slug: # Если в запросе от пользователя есть параметр на фильтрацию, то
        category = get_object_or_404(Category, slug=category_slug) # мы получаем с базы данных категории с помощью get_object_or_404
        products = products.filter(category=category) # далее мы все продукты, которые у нас есть, фильтруем по выбранной категории

    return render(request, 'main/product/list.html',  # возвращаем юзеру шаблон страницы и третим параметром передаем context, именно эти параметры позволяют нам обращаться к категориям или продуктам
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug): # страница товара, более подробно 
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category, # так же предлагаем похожие продукты пользователю
                                              available=True).exclude(id=product.id)[:4] # c помощью exclude мы исключаем id того продукта, который уже выбрал польльзователь
    
    return render(request, 'main/product/detail.html', {'product': product,
                                                        'related_products': related_products})