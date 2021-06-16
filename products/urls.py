from django.urls    import path

from products.views import ProductDetail


urlpatterns = [
    path('/<int:product_id>', ProductDetail.as_view()),
    
]
