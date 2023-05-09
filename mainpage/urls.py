from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('current_products/<int:pk>', views.current_products),
    path('category/<int:pk>', views.get_exact_category),
    path('item/<int:pk>', views.exact_product),
    path('cart', views.get_user_cart),
    path('order', views.complete_order)
]