from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Material, ProductInstance, Order

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Material)
admin.site.register(ProductInstance)
admin.site.register(Order)