from django.shortcuts import render
from django.views import generic

from store.models import Product, ProductImage, ProductInstance, Order, Material
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

class ProductListView(generic.ListView):
    model = Product
    context_object_name = "products"
class ProductDetailView(generic.DetailView):
    model = Product