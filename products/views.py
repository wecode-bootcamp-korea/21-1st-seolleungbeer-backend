from itertools             import chain
from django.db.models.expressions import OuterRef
from django.db.models.fields import CharField
from django.db.models.query_utils import subclasses

from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import EmptyPage
from django.db.models      import Q, When, Case, Exists,Value

from .models import Category, SubCategory, Product, ProductInfo, ProductImage, ImageType

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        result     = {}

        for category in categories:
            result[category.english_name] = [sub.english_name for sub in category.sub_category_set.all()]

        return JsonResponse(result, status=200)

class ProductListView(View):
    def get(self, request):
        offset        = int(request.GET.get('offset',0))
        limit         = int(request.GET.get('limit',6))
        category      = request.GET.get('category')
        subcategories = request.GET.get('subcategory')

        if subcategories:
            q = Q(sub_category__english_name=subcategories)
            print(q)
        elif category:
            q = Q(sub_category__category__english_name=category)
        else:
            q = Q()

        products         = Product.objects.filter(q).order_by('id')
        products_in_page = products[offset:(offset+limit)]
        message          = int(products.count() <= (offset+limit))
        result           = {}
        result_list      = []

        for product in products_in_page:
            image     = product.productimage_set.filter(image_type__type="1000*1000").first()
            image_url = image.image_url if image else image
            result    = {
                'id'           : product.id,
                'korean_name'  : product.korean_name,
                'english_name' : product.english_name,
                'price'        : product.price,
                'image'        : image_url
            }
            result_list.append(result)
        return JsonResponse({'message':message, 'content':result_list}, status=200)

class ProductDetail(View):
    def get(self, request, product_id):
        try:
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'MESSAGE' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)

            product = Product.objects.get(id=product_id)

            result={
                'korean_name'  : product.korean_name,
                'english_name' : product.english_name,
                'price'        : product.price,
                'description'  : product.description,
                'image'        :[{
                    'image_url'  : image.image_url,
                    'image_type' : image.image_type.type
                    }

            for image in product.productimage_set.all()],

                'info'         :{
                'meterial'     : product.product_info.meterial,
                'size'         : product.product_info.size,
                'manufacturer' : product.product_info.manufacturer,
                'made'         : product.product_info.made,
                'distributor'  : product.product_info.distributor,
                'afterservice' : product.product_info.afterservice
                }}

            return JsonResponse({'result':result},status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
