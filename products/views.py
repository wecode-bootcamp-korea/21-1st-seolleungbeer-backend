import json

from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import EmptyPage, Paginator

from .models import Category, SubCategory, Product, ProductInfo, ProductImage, ImageType

class ProductListView(View):
    def get(self, request):
        try:        
            # get_query_parameter
            offset        = int(request.GET.get('offset') or 0)
            limit         = int(request.GET.get('limit') or 6)
            category      = request.GET.get('category')
            subcategories = request.GET.get('subcategory')
    
            # filtering
            products = []

            if category == '' or category == None:
                products = Product.objects.all()
            
            elif subcategories == '' or subcategories == None:
                category = Category.objects.get(name=category)
                subcategories = SubCategory.objects.filter(category=category)

                for sub in subcategories:
                    products_in_sub = Product.objects.filter(sub_category=sub)
                    
                    for product in products_in_sub:
                        products.append(product)

            else:
                subcategories = SubCategory.objects.get(name=subcategories)
                products_in_sub = Product.objects.filter(sub_category=subcategories)

                for product in products_in_sub:
                    products.append(product)            
            
            #paging 다시
            products_in_page = products[offset:(offset+limit)]
            print(offset,limit)
            print(products_in_page)

            # make_response
            result = {}
            result_list = []

            for product in products_in_page:
                
                p = Product.objects.get(korean_name="선릉탈출 보드게임")
                image = ProductImage.objects.get(product=p, image_type_id=1)
                
                result = {
                    'id'           : product.id,
                    'korean_name'  : product.korean_name,
                    'english_name' : product.english_name,
                    'price'        : product.price,
                    'image'        : image.image_url
                }
                result_list.append(result)
            
            return JsonResponse(result_list, status=200, safe=False)
        
        except Category.DoesNotExist:
            return JsonResponse({'message':'DoesNotExist, category'}, status=400)

        except Category.MultipleObjectsReturned:
            return JsonResponse({'message':'MultipleObjects, category'}, status=400)

        except SubCategory.DoesNotExist:
            return JsonResponse({'message':'DoesNotExist, subcategory'}, status=400)

        except SubCategory.MultipleObjectsReturned:
            return JsonResponse({'message':'MultipleObjects, subcategory'}, status=400)

        except Product.MultipleObjectsReturned:
            return JsonResponse({'message':'DoesNotExist, product'}, status=400)

        except ProductImage.DoesNotExist:
            return JsonResponse({'message':'DoesNotExist, image'}, status=400)

        except ProductImage.MultipleObjectsReturned:
            return JsonResponse({'message':'MultipleObjects, image'}, status=400)

        except EmptyPage:
            return JsonResponse({'message':'EmptyPage'}, status=404)

class CategoryViw(View):
    def get(self, request):
        try:
            categories = Category.objects.all()
            result = {}

            for category in categories:
                subcategories = SubCategory.objects.all()
                subs_in_category = []

                for sub in subcategories:
                    subs_in_category.append(sub)            

                result[category.name] = subs_in_category

            return JsonResponse({'message':result}, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({'message':'DoesNotExist'}, status=400)

        except SubCategory.DoesNotExist:
            return JsonResponse({'message':'DoesNotExist'}, status=400)

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






# 오류 리스트업
# get하는 모든 DB table에 대해 DoesNotExist, MultipleObjectsReturned
# filter하는 모든 DB table에 대해 DoesNotExist
# Paginator에 대해 페이지의 범위를 벗어났을 때 EmptyPage (더 적게든 더 많게든)
# request.메서드(GET,POST등)에 대해, '.get(Key값)' 메서드를 쓸 경우 오류가 날 일이 없음 1) Key값이 있으면 Value값 2)Key값이 없으면 None 반환
# request의 body가 json에 담겨서 오는 경우에 대해, Json.DecodeError

# 참고(1): 왜 filter에는 MultipleObjectsReturned가 필요없는가?
# QuerySet이라는 배열에 담겨 반환되기 때문이다. 배열이므로 1개든 100개든 상관 없음

# 참고(2): 'request.GET'이란?
# request.메서드(GET, POST등)은 'QueryDict' object이며, Key값으로 Value값을 가져오고 싶은 경우 '.get('Key값')을 쓸 수 있다
# QueryDict오브젝트.get(Key값)과, QueryDict오브젝트[Key값]의 차이는, 전자는 Key가 없으면 None 반환, 후자는 Key가 없으면 오류 발생한다는 것
# 즉 Key가 있을 수도 없을 수도 있는 optional인 경우, 전자를 선택하는 것이 좋다.

# Query Parameter 규칙 대강

# 논의할 사항
# 0. 규칙 전반

# 1. param값이 없는 경우, redirect하여 요청이 가능한가?
# 가능하다면 param값이 빠진 경우, 무조건 param값을 추가하여 요청을 보낼 수 있도록 해줘야 할 것 같은데
# 예를 들어, /products?category=& 로 들어오면 >>/products?category=&subcategory=&page=1 로 수정하여 요청
# 유저가 url을 직접바꾸거나 한 경우 이런 경우가 있을 수 있음
# 백에서도 None인 경우에 그에 맞는 리소스 반환되도록 하여, 이중처리

# 2. 알럿 띄우는 것이 가능한가?
# 가능하다면 에러 메세지 뜬 경우, 최대한 알럿 >> 상품 메인으로 리다이렉트

# 3. 요청을 2개로 나눠서 보내줄 수 있는가?
# SHOP 클릭 시, 1)카테고리 정보 요청과 2)상품리스트 요청
# 검색 클릭 시에는 2)상품리스트 요청만 다시 (1은 그대로 재사용)

# 4. 이미지 없는 경우, 디폴트 이미지를 보내주는 것이 나은가 아니면 이미지Key/Value를 아예 빼고 보내주는 것이 나은가?

# 기본 url: /shop

# 1) 'SHOP' 메뉴를 클릭한 경우 param 없음(카테/서브/페이지 전부)
# /products

# 2) 필터링
# '검색'을 클릭한 이후 param 항상 있음(카테,서브,페이지 전부)
# 카테,서브 디폴트는 빈스트링, 페이지 디폴트는 1
# /products?category=&subcategory=&page=1
# 2-1) 필터링이 전체인 경우, Key값 있고 Value값 빈스트링
# /products?category=&subcategory=&page=1
# 2-2) 필터링을 선택한 경우, Key값 있고 Value값 있음
# /products?category=술&subcategory=맥주&page=1

# 즉, 한 번 검색을 클릭한 이후에는 무조건 param이 있음
# 즉, shop 버튼 클릭시 없고 '검색'버튼 클릭 시 있음

# 에러처리: 카테에 맞는 Product가 없는 경우 >> "상품이 없습니다" 페이지 or "상품이 없습니다" 알럿 후 상품디폴트페이지로 리다이렉트 
# 에러처리: 카테,서브카테고리가 오류나는 경우(없거나 너무 많거나) >> "잘못된 카테고리입니다" 알럿 후 상품디폴트페이지로 리다이렉트

# 3) 페이지
# '페이지'를 클릭한 이후 param 항상 있음(카테,서브,페이지 전부)
# 카테,서브 디폴트는 빈스트링, 페이지 디폴트는 1
# /products?category=&subcategory=&page=1
# 3-1) LOAD MORE 클릭했을 경우, 페이지 추가됨
# /products?category=&subcategory=&page=3&page=4
# 3-2) 다시 1페이지를 누를 경우, 페이지 = 1
# /products?category=&subcategory=&page=1

# 에러처리: EmptyPage인 경우(오류) >> "페이지가 없습니다" 알럿 후 상품디폴트페이지로 리다이렉트 ??

# PR전 최종 점검
# 컨벤션은 push하기 직전에 최종적으로 맞추고 올리자
