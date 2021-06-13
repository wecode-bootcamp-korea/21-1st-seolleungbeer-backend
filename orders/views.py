from django.views    import View
from django.http     import JsonResponse

from .models         import Order, OrderItem
from products.models import ProductImage

# from users.utils import user_decorator

class CartView(View):
    # @user_decorator
    def get(self, request):
        try:
            user       = request.user
            order_item = OrderItem.objects.filter(orders_user = user, order_statuses_status = '주문 전')

            for carts in order_item:
                carts_list = {
                    'cart_id'         : carts.id,
                    'product_image'   : ProductImage.image_url,
                    'amount'          : carts.amount,
                    'korean_name'     : carts.product.korean_name,
                    'english_name'    : carts.product.english_name,
                    'delivery_charge' : carts.order.delivery_charge,
                    'payment_charge'  : carts.order.payment_charge,
                    'delivery_method' : carts.order.delivery_method,
                    'like'            : carts.order.user.like
                }

            return JsonResponse({'message':'SUCCESS', 'result':carts_list}, status=200)
        
        except Order.DoesNotExist:
            return JsonResponse({'message': 'NOTHING_IN_CART'}, status=400)