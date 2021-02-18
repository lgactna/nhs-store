from django.shortcuts import render
from django.views import generic

from store.models import Product, ProductImage, ProductInstance, Order, Material
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

    try:
        request.session['cart'][str(time.time())] = "b"
        request.session.modified = True
    except:
        cart = request.session.get('cart', {"dog":"bat"})
        request.session['cart'] = cart

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def cart(request):
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