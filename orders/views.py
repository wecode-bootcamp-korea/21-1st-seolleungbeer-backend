from django.views    import View
from django.http     import JsonResponse

from .models         import Order, OrderItem
from users.utils     import user_decorator

class CartView(View):
    @user_decorator
    def get(self, request):
        try:
            user       = request.user
            order_item = OrderItem.objects.filter(order__user = user, order__order_status__status="주문 전")
            result     = []

            for carts in order_item:
                carts_list = {
                    'cart_id'         : carts.id,
                    'amount'          : carts.amount,
                    'korean_name'     : carts.product.korean_name,
                    'english_name'    : carts.product.english_name,
                    'delivery_charge' : carts.order.delivery_charge,
                    'payment_charge'  : carts.product.price,
                    'delivery_method' : carts.order.delivery_method
                }
                result.append(carts_list)

            return JsonResponse({'message':'SUCCESS', 'result':result}, status=200)
        
        except Order.DoesNotExist:
            return JsonResponse({'message': 'NOTHING_IN_CART'}, status=400)