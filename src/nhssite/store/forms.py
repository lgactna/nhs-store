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

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    student_id = forms.CharField(max_length=10)
    email = forms.EmailField()
    #phone is not standardized - a human will be contacting anyways
    phone = forms.CharField(max_length=15)
    special_instructions = forms.CharField(required=False)
class CustomOrderForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    student_id = forms.CharField(max_length=10)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    custom_links = forms.CharField()
    custom_quantity = forms.IntegerField()
    custom_material = forms.IntegerField()
    special_instructions = forms.CharField(required=False)
