# файл для добавления в корзину товаров

from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=20, initial=1, # тут мы создаем форму, куда юзер может вписать нужное ему количество товара
                                  widget = forms.NumberInput(attrs={'class': 'form-control'}))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)