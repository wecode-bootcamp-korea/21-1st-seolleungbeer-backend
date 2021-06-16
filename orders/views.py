from django.views    import View
from django.http     import JsonResponse

from .models         import OrderItem, OrderStatus
from users.utils     import user_decorator

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
                    'delivery_method' : carts.order.delivery_method
                } for carts in order_item]

            return JsonResponse({'message':'SUCCESS', 'result':result}, status=200)
        
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'NOTHING_IN_CART'}, status=400)