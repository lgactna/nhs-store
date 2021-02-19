from django.shortcuts import render
from django.views import generic

from store.models import Product, ProductImage, ProductInstance, Order, Material
from store.forms import CartForm, CheckoutForm
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
            "item_cost": item_cost
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

    context = generate_cart_context(request)
    #show cart page here...
    return render(request, 'cart.html', context=context)

def cart_delete(request):
    pass

def checkout(request):
    context = generate_cart_context(request)
    return render(request, 'checkout.html', context=context)

def confirmation(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            order_obj = Order(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                student_id = form.cleaned_data['student_id'],
                email = form.cleaned_data['email'],
                phone = form.cleaned_data['phone'],
                extra_notes = form.cleaned_data['extra_notes'],
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
            
            request.session['cart'] = {}
            return render(request, 'index.html')
    else:
        return cart(request)

def custom_ordering(request):
    pass

class ProductListView(generic.ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/catalog.html"
class ProductDetailView(generic.DetailView):
    model = Product