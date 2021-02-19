from django import forms

class CartForm(forms.Form):
    quantity = forms.IntegerField()
    material = forms.IntegerField()
    product_id = forms.IntegerField()

    def clean_quantity(self):
        quantity_input = self.cleaned_data['quantity']
        if quantity_input <= 0:
            quantity_input = 1
        return quantity_input
