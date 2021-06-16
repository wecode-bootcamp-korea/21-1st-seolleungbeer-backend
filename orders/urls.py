from django.urls import path

from .views      import PaymentView,CartView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/payment',PaymentView.as_view())
]
