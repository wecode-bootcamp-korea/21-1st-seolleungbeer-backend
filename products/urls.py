from django.urls    import path

from products.views import ProductDetail, ProductListView


urlpatterns = [
    path('/<int:product_id>', ProductDetail.as_view()),
    path('', ProductListView.as_view())
]
