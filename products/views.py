import json

from django.http  import JsonResponse
from django.views import View

from .models import Product, ProductImage, ProductInfo, ImageType,SubCategory

class ProductDetail(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            result=[]
            images = product.productimage_set.all()
            image_list = [{
                'image_url'  : image.image_url,
                'image_type' : image.image_type.type
            }for image in images]

            result.append({
                'korean_name'  : product.korean_name,
                'english_name' : product.english_name,
                'price'        : product.price,
                'description'  : product.description,
                'image'        : image_list,

                'info'         :{
                    'meterial'     : product.product_info.meterial,
                    'size'         : product.product_info.size,
                    'manufacturer' : product.product_info.manufacturer,
                    'made'         : product.product_info.made,
                    'distributor'  : product.product_info.distributor,
                    'afterservice' : product.product_info.afterservice
                }})

            return JsonResponse({'result':result},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)