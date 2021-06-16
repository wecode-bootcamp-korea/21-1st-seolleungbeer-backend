from django.urls import path

from .views      import PaymentView,CartView

urlpatterns = [
    path('/payment', PaymentView.as_view()),
    path('/cart', CartView.as_view())
]
