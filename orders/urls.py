from django.urls import path

from .views      import OrderView,CartView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('',OrderView.as_view())
]
