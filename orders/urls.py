from django.urls import path

from .views      import CartView

urlpatterns = [
    path('/cart-get', CartView.as_view())
]
