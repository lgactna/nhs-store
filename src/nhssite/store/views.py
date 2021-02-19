from django.shortcuts import render
from django.views import generic

from store.models import Product, ProductImage, ProductInstance, Order, Material
from store.forms import CartForm
import time
# Create your views here.

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
    try:
        request.session['cart']
    except:
        cart = request.session.get('cart', {})
        request.session['cart'] = cart
    
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

    cart_contents = []
    total_cost = 0
    new_item = None

    for cart_id, cart_item in request.session['cart'].items():
        product_obj = Product.objects.get(id=cart_item['product_id'])
        material_obj = Material.objects.get(id=cart_item['material'])
        item_cost = int(cart_item['quantity'])*product_obj.price
        cart_dict = {
            "product": product_obj,
            "quantity": cart_item['quantity'],
            "material": material_obj,
            "item_cost": item_cost
        }
        total_cost += item_cost

        if cart_id == new_item_id:
            new_item = cart_dict
        else:
            cart_contents.append(cart_dict)

    context = {
        "cart_contents": cart_contents,
        "total_cost": total_cost,
        "new_item": new_item
    }
    #show cart page here...
    return render(request, 'cart.html', context=context)

def cart_delete(request):
    pass

def checkout(request):
    pass

def confirmation(request):
    pass

def custom_ordering(request):
    pass
class ProductListView(generic.ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/catalog.html"
class ProductDetailView(generic.DetailView):
    model = Product