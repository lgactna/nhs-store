from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Material, ProductInstance, Order

#admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Material)
admin.site.register(ProductInstance)
#admin.site.register(Order)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'available')
    list_filter = ('available',)

    inlines = [ProductImageInline]

class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'created_at', 'grand_total', 'fulfilled')
    list_filter = ('created_at', 'updated_at', 'fulfilled')

    inlines = [ProductInstanceInline]

    readonly_fields = ('created_at', 'updated_at')

    '''
    fieldsets = (
        ('Student Info', {
            'fields': (('first_name', 'last_name', 'student_id'), 
                       ('email', 'phone'))
        }),
        ('Order Details', {
            'fields': (('grand_total','created_at', 'updated_at'),
                       ('extra_notes',),
                       ('fulfilled'))
        }),
    )
    '''