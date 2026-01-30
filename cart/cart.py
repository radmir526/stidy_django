# В этом файле запишем всю основную логику работы корзины 

from django.conf import settings
from main.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID) # получаем сессию пользователя
        if not cart: # если у пользователя нет корзины
            cart = self.session[settings.CART_SESSION_ID] = {} # то мы просто задаем пустой кортеж
        self.cart = cart # если корзина есть, то она остается с теми товарами, которые юзер добавил


    def add(self, product, quantity=1, override_quantity=False): # Метод добавления 
        product_id = str(product.id)
        if product_id not in self.cart: # если айди продукта не находится в корзине 
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity: # Если человек написал сам добавить 10 товаров, то мы их просто добавляем
            self.cart[product_id]['quantity'] = quantity
        else: # Если человек нажимает просто плюсик по одному, то есть он добавляет товар по одному, то мы просто прибавляем к количествую
            self.cart[product_id]['quantity'] += quantity
        self.save()


    def save(self): # функция которая сохраняет корзину 
        self.session.modified = True


    def remove(self, product): # уадаление продуктов из корзины 
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self): # эта функция проходится по корзине и выводит все свойства товаров и позволяет с ними работать
        product_ids = self.cart.keys() # сохраняем все айдишники товаров в корзине 
        products = Product.objects.filter(id__in=product_ids) # берем только те продукты, которые находятся в корзине 
        cart = self.cart.copy() # дополнительно сохраняем

        for product in products: # проходимся по всем товарам 
            cart[str(product.id)]['product'] = product # и записываем все продукты по их айди и ключу product

        for item in cart.values(): # прописываем параметры наших товаров в козине
            item['price'] = float(item['price']) # цена для одного товара 
            item['total_price'] = item['price'] * item['quantity'] # цена для нескольких товаров
            yield item

    
    def __len__(self): # метод для подсчета количества товаров в корзине 
        return sum(item['quantity'] for item in self.cart.values()) # возвращаем сумму количества товаров 
    

    def get_total_price(self): # метод для вывода общей  стоимости корзины 
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values()) # возвращаем сумму всех товаров в корзине 
    

    def clear(self): # метод для отчистки корзины 
        del self.session[settings.CART_SESSION_ID] # удаляем сессию которая отвечает за корзину
        self.save()