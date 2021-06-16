from django.urls    import path

from products.views import ProductDetail, ProductListView, CategoryListView


urlpatterns = [
<<<<<<< HEAD
    path('/<int:product_id>', ProductDetail.as_view()),
    
=======
    path('/category', CategoryListView.as_view()),
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetail.as_view())
>>>>>>> main
]
