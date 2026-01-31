from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# -------------------------------
# Добавление товара в корзину
# -------------------------------
@require_POST  # запрет GET-запросов, только POST
def cart_add(request, product_id):
    cart = Cart(request)  # создаём объект корзины, привязанный к сессии пользователя
    product = get_object_or_404(Product, id=product_id)  # получаем объект товара или 404
    form = CartAddProductForm(request.POST)  # создаём форму с данными из POST

    if form.is_valid():  # проверяем форму
        cd = form.cleaned_data  # очищенные данные формы
        # добавляем товар в корзину
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']  # True если пользователь хочет заменить количество
        )
        # после добавления — перенаправляем на страницу корзины
        return redirect('cart:cart_detail')


# -------------------------------
# Удаление товара из корзины
# -------------------------------
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)  # объект корзины
    product = get_object_or_404(Product, id=product_id)  # находим товар
    cart.remove(product)  # удаляем его из корзины
    return redirect('cart:cart_detail')  # возвращаемся на страницу корзины


# -------------------------------
# Отображение корзины
# -------------------------------
def cart_detail(request):
    cart = Cart(request)  # объект корзины

    # Добавляем к каждому товару форму для обновления количества
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],  # текущее количество
            'override': True,  # при отправке формы заменяем количество, а не прибавляем
        })

    # Рендерим страницу корзины
    return render(request, 'cart/cart_detail.html', {'cart': cart})
