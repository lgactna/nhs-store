from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.ProductListView.as_view(), name='catalog'),
    path('item/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('cart-delete/', views.cart_delete, name='cart-delete'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('custom-ordering/', views.custom_ordering, name='custom-ordering'),
    path('custom-confirmation/', views.custom_confirmation, name='custom-confirmation')
]

handler404 = 'store.views.page_not_found_view'