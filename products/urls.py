from django.urls    import path

from products.views import CategoryListView, ProductDetail,ProductListView


urlpatterns = [
    path('/category',CategoryListView.as_view()),
    path('/<int:product_id>', ProductDetail.as_view()),
    path('', ProductListView.as_view()),
]
