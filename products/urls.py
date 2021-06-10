from django.urls import path
from .views      import ProductListView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/list', ProductListView.as_view())
]