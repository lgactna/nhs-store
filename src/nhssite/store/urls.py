from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.ProductListView.as_view(), name='catalog'),
    path('item/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
]
