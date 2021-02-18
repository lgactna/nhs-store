from django import forms

class CartForm(forms.Form):
    quantity = forms.IntegerField()
    material = forms.IntegerField()
    product_id = forms.IntegerField()