from django.urls import path

from .views      import OrderView,CartView

urlpatterns = [
    path('/order', OrderView.as_view()),
    path('/cart', CartView.as_view())
]
