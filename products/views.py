from itertools             import chain

from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import EmptyPage

from .models import Category, SubCategory, Product, ProductInfo, ProductImage, ImageType

class CategoryListView(View):
    def get(self, request):
        try:
            categories = Category.objects.all()
            result     = {}

            for category in categories:
                subcategories = SubCategory.objects.filter(category=category)
                result[category.english_name] = [sub.english_name for sub in subcategories]

            return JsonResponse(result, status=200)
        
        except Category.DoesNotExist or SubCategory.DoesNotExist:
            return JsonResponse({'message':'Category Does Not Exist'}, status=400)

class ProductListView(View):
    def get(self, request):
        try:        
            # get_query_parameter
            offset        = int(request.GET.get('offset') or 0)
            limit         = int(request.GET.get('limit') or 6)
            category      = request.GET.get('category')
            subcategories = request.GET.get('subcategory')
    
            # filter
            products = []

            if category == '' or category == None:
                products = Product.objects.all()
            elif subcategories == '' or subcategories == None:
                category       = Category.objects.get(english_name=category)
                subcategories  = SubCategory.objects.filter(category=category)
                products       = []

                for sub in subcategories:
                    products_in_subs = Product.objects.filter(sub_category=sub)                   
                    products = list(chain(products, products_in_subs))
            else:
                subcategories = SubCategory.objects.get(english_name=subcategories)
                products      = Product.objects.filter(sub_category=subcategories)

            # check_product_amount        
            if len(products) == 0:
                return JsonResponse({'message':'Product Does Not Exist'}, status=400)      
            elif len(products) <= offset:
                return JsonResponse({'message':'EmptyPage'}, status=404)            
            elif len(products) <= offset+limit:
                message = 'Last Page'
            else:
                message = 'Page Left'

            # paging
            products_in_page = products[offset:(offset+limit)]

            # make_response
            result      = {}
            result_list = []

            for product in products_in_page:
                image_type  = ImageType.objects.get(type="1000*1000")
                image       = ProductImage.objects.filter(product=product, image_type=image_type)

                # chechk_image_amount
                if len(image) == 0:
                    image_url = "No Image"                  
                elif len(image) == 1:
                    image_url = image[0].image_url
                else:
                    return JsonResponse({'message':'Image Multiple Objects Returned'}, status=400)

                result = {
                    'id'           : product.id,
                    'korean_name'  : product.korean_name,
                    'english_name' : product.english_name,
                    'price'        : product.price,
                    'image'        : image_url
                }
                result_list.append(result)
            
            return JsonResponse({'message':message,'content':result_list}, status=200)
        
        except Category.DoesNotExist or SubCategory.DoesNotExist:
            return JsonResponse({'message':'Category Does Not Exist'}, status=400)

        except Category.MultipleObjectsReturned or SubCategory.MultipleObjectsReturned:
            return JsonResponse({'message':'Category Multiple Objects Returned'}, status=400)

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
                    }for image in product.productimage_set.all()],

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
