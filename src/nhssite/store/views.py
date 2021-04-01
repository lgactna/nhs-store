from django.shortcuts import render
from django.views import generic
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from store.models import Product, ProductImage, ProductInstance, Order, Material
from store.forms import CartForm, CheckoutForm, CustomOrderForm, CartDeleteForm
import time
# Create your views here.

def generate_cart_context(request, *, new_item_id=None):
    cart_contents = []
    total_cost = 0
    total_quantity = 0
    new_item = None

    for cart_id, cart_item in request.session['cart'].items():
        product_obj = Product.objects.get(id=cart_item['product_id'])
        material_obj = Material.objects.get(id=cart_item['material'])
        item_cost = int(cart_item['quantity'])*product_obj.price
        cart_dict = {
            "product": product_obj,
            "quantity": int(cart_item['quantity']),
            "material": material_obj,
            "item_cost": item_cost,
            "cart_id": cart_id
        }
        total_cost += item_cost
        total_quantity += cart_item['quantity']

        if cart_id == new_item_id:
            new_item = cart_dict
        else:
            cart_contents.append(cart_dict)

    context = {
        "cart_contents": cart_contents,
        "total_cost": total_cost,
        "total_quantity": total_quantity,
        "new_item": new_item
    }

    return context

def index(request):
    """View function for home page of site."""

    # Get featured products so they can be shown on home page
    featured_products = Product.objects.filter(featured=True)

    context = {
        'featured_products': featured_products
    }
    for product in featured_products:
        for pimage in product.images.all():
            print(pimage.image.url)

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def cart(request):
    new_item_id = str(time.time())

    if request.method == "POST":
        form = CartForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            cart_item = {
                "product_id": form.cleaned_data['product_id'],
                "quantity": form.cleaned_data['quantity'],
                "material": form.cleaned_data['material'],
            }
            request.session['cart'][new_item_id] = cart_item
            request.session.modified = True

    context = generate_cart_context(request, new_item_id=new_item_id)
    #show cart page here...
    return render(request, 'cart.html', context=context)

def cart_delete(request):
    context = generate_cart_context(request)
    if request.method == "POST":
        form = CartDeleteForm(request.POST)
        if form.is_valid():
            
            cart_id = form.cleaned_data["cart_id"]
            if cart_id == "0":
                request.session['cart'] = {}
                context['alert_message'] = "Cleared cart."
                return render(request, 'cart.html', context=context)
            else:
                try:
                    product_obj = Product.objects.get(id=request.session['cart'][cart_id]["product_id"])
                    del request.session['cart'][cart_id]
                    request.session.modified = True

                    context['alert_message'] = f"Removed {product_obj}."
                    return render(request, 'cart.html', context=context)
                except: 
                    context['alert_message'] = "Failed to remove cart item."
                    return render(request, 'cart.html', context=context)
        else:
            print("c")
            context['alert_message'] = "Failed to remove cart item."
            return render(request, 'cart.html', context=context)
    else:
        #ignore if not post
        context = generate_cart_context(request)
        return render(request, 'cart.html', context=context)

def checkout(request):
    context = generate_cart_context(request)
    return render(request, 'checkout.html', context=context)

def confirmation(request):
    if request.method == "POST":
        #protection against refreshing or posts with empty cart
        if len(request.session['cart']) == 0:
            context = generate_cart_context(request)
            context['alert_message'] = "You have to order something first before you can get a confirmation. 🤔"
            return render(request, 'cart.html', context=context)

        form = CheckoutForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            order_obj = Order(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                student_id = form.cleaned_data['student_id'],
                email = form.cleaned_data['email'],
                phone = form.cleaned_data['phone'],
                special_instructions = form.cleaned_data['special_instructions'],
                grand_total = 0.0
            )
            order_obj.save()

            grand_total = 0
            for cart_id, cart_item in request.session['cart'].items():
                product_obj = Product.objects.get(id=cart_item['product_id'])
                material_obj = Material.objects.get(id=cart_item['material'])
                price = int(cart_item['quantity'])*product_obj.price
                grand_total += price

                product_instance = ProductInstance(
                    product = product_obj,
                    material = material_obj,
                    quantity = int(cart_item['quantity']),
                    total_price = price,
                    order = order_obj
                )
                product_instance.save()
            order_obj.grand_total = grand_total
            
            context = generate_cart_context(request)
            context["order"] = order_obj

            send_confirmation_email(context, form.cleaned_data['email'])

            request.session['cart'] = {}
            return render(request, 'confirmation.html', context=context)
    else:
        context = generate_cart_context(request)
        context['alert_message'] = "You have to order something first before you can get a confirmation. 🤔"
        return render(request, 'cart.html', context=context)

def custom_ordering(request):
    context = {"materials": Material.objects.all()}
    return render(request, 'custom-ordering.html', context=context)

def custom_confirmation(request):
    if request.method == "POST":
        form = CustomOrderForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            material_id = form.cleaned_data['custom_material']

            order_obj = Order(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                student_id = form.cleaned_data['student_id'],
                email = form.cleaned_data['email'],
                phone = form.cleaned_data['phone'],
                is_custom = True,
                custom_links = form.cleaned_data['custom_links'],
                custom_quantity = form.cleaned_data['custom_quantity'],
                custom_material = Material.objects.get(id=material_id) if material_id != -1 else None,
                special_instructions = form.cleaned_data['special_instructions'],
                grand_total = 0.0
            )
            order_obj.save()

            context = {"order": order_obj}

            send_confirmation_email(context, form.cleaned_data['email'])
            
            return render(request, 'confirmation.html', context=context)
    else:
        return custom_ordering(request)

def send_confirmation_email(context, order_email):
        #always send notifying email to the master email
        subject = f'Order #{context["order"].id} was placed'
        html_message = render_to_string('email-conf.html', context)
        plain_message = strip_tags(html_message)
        to = "store.aactnhs@gmail.com" #consider using constance in the future for a list of "always notify" emails
        from_email = None #uses DEFAULT_FROM_EMAIL in settings.py

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        #if defined, send conf to student's email
        if order_email:
            subject = f'Confirmation of order #{context["order"].id}'
            mail.send_mail(subject, plain_message, from_email, [order_email], html_message=html_message)
    

class ProductListView(generic.ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/catalog.html"

class ProductDetailView(generic.DetailView):
    model = Product

def page_not_found_view(request, exception):
    return render(request, '404.html')