import json

from django.views     import View
from django.http      import JsonResponse

from users.utils     import user_decorator
from orders.models   import OrderItem, OrderStatus

class CartView(View):
    @user_decorator
    def get(self, request):
        try:
            user       = request.user
            order_item = OrderItem.objects.filter(
                order__user            = user, 
                order__order_status_id = OrderStatus.PENDING
            )
            
            result     = [{
                    'order_id'        : carts.order.id,
                    'cart_id'         : carts.id,
                    'amount'          : carts.amount,
                    'korean_name'     : carts.product.korean_name,
                    'english_name'    : carts.product.english_name,
                    'delivery_charge' : carts.order.delivery_charge,
                    'payment_charge'  : carts.product.price,
                    'product_image'   : carts.product.main_image,
                    'delivery_method' : carts.order.delivery_method
                } for carts in order_item]

            return JsonResponse({'message':'SUCCESS', 'result':result}, status=200)
        
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'NOTHING_IN_CART'}, status=400)

    @user_decorator
    def delete(self, request):
        try:
            data       = json.loads(request.body)
            order_item = OrderItem.objects.filter(id__in=data['cart_item_id'])

            order_item.delete()
            
            return JsonResponse({'message':'DELETE_SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'INVAILD_VALUE'}, status=400)
        
        except ValueError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)