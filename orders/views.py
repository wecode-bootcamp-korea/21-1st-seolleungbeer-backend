from django.views          import View
from django.http           import JsonResponse
from django.db             import IntegrityError
from django.core.paginator import Paginator

from .models import Category, SubCategory, Product, ProductImage, ProductInfo

def get(self, request):
    try:

        # 요청에서 온 페이지 
        page = int(request.GET.get('page'))
        category = request.GET.get('category')
        sub_category = request.GET.get('sub_category')
        products = []

        if category == None or category == 'all':
            products = Product.objects.all()
        
        elif sub_category== None or sub_category == 'all':
            sub_category = SubCategory.objects.filter(name=category)yy
            
            for sub in sub_category:
                products.append(Product.objects.filter(sub_category=sub))

        else:
            sub_category = SubCategory.objects.filter(name=sub_category)
            products = Product.objects.filter(sub_category=sub_category)

        pagination = Paginator(products, 4)

        # 응답 만들기
        result = {}
        result_list = []

        for product in pagination.page(page):
            
            #쿼리셋 말고 object 반환
            images = ProductImage.objects.filter(product=product, image_type='1000*1000')

            for image in images:
                image = image
            
            result = {
                'korean_name'  : product.korean_name,
                'english_name' : product.english_name,
                'price'        : product.price,
                'image'        : image
            }
            result_list.append(result)
        
        return JsonResponse({'message':result_list}, status=200)
    except:
        return JsonResponse({'message':'에러 처리'}, status=400)

