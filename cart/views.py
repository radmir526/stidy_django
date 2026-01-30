from django.shortcuts import render  , redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .froms import CartAddProductForm


@require_POST
def cart_add(request, product_id): # пишем функцию, которая обрабатывает наш запрос на добавление товара в корзину
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid(): # если с формой все хорошо, то мы берем данные с формы
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], 
                 override_quantity=cd['override'])  
        return redirect('cart:cart_detail') # после добавления возвращаемся на страницу корзины 
    


#Метод удаления товаров из корзины
@require_POST
def cart_remove(request, product_id):
    cart =Cart(request) # Создается объект корзины, привязанный к текущему пользователю.
    product = get_object_or_404(Product, id=product_id) # получаем товар из базы
    cart.remove(product) # удаляем корзину
    return redirect('cart:cart_detail') # после удаления возвращаемся на страницу корзины


def cart_detail(request): # эта фугкция отвечает за показ страницы нашей корзины
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quatntity': item['quantity'],
            'override': True,
        })
    return render(request, 'cart/cart_detail.html', {'cart': cart}) # Возвращаем шаблон страницы нашей корзины