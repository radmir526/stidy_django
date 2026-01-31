# В этом файле описана логика работы корзины

from django.conf import settings
from main.models import Product


class Cart:
    def __init__(self, request):
        # Получаем сессию пользователя
        self.session = request.session

        # Пытаемся получить корзину из сессии
        cart = self.session.get(settings.CART_SESSION_ID)

        # Если корзины нет — создаём пустую
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        # Сохраняем корзину в объекте класса
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Добавление товара в корзину
        :param product: объект Product
        :param quantity: количество
        :param override_quantity: если True, заменяем существующее количество
        """
        product_id = str(product.id)

        # Если товар ещё не в корзине — создаём запись
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        # Если передано override_quantity — заменяем количество
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            # Иначе прибавляем количество
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """Сохраняем корзину в сессии"""
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Проходимся по корзине для шаблонов и расчёта сумм
        Добавляем объект Product к каждому элементу
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            # Добавляем объект Product для удобства
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = float(item['price'])  # цена одного товара
            item['total_price'] = item['price'] * item['quantity']  # общая цена
            yield item  # позволяет использовать Cart как итератор

    def __len__(self):
        """Общее количество товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Общая стоимость корзины"""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очистка корзины"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
