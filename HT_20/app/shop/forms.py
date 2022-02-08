from django import forms


class ProductForm(forms.Form):
    brand = forms.CharField(label='brand', max_length=20)
    model = forms.CharField(label='model', max_length=20)
    category = forms.CharField(label='category', max_length=10)


class AddToCartProductForm(forms.Form):
    brand = forms.CharField(label='brand', max_length=20)
    model = forms.CharField(label='model', max_length=20)
    category = forms.CharField(label='category', max_length=10)
    amount = forms.CharField(label='amount', max_length=1)


class EditProductForm(forms.Form):
    brand = forms.CharField(label='brand', max_length=20)
    model = forms.CharField(label='model', max_length=100)
    description = forms.CharField(label='description')
    price = forms.IntegerField(label='price')
    available = forms.CharField(label='available', max_length=3)
    old_brand = forms.CharField(label='old_brand', max_length=20)
    old_model = forms.CharField(label='old_model', max_length=100)
    category = forms.CharField(label='category', max_length=10)
    amount = forms.IntegerField(label='amount')
