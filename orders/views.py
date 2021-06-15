import json, uuid

from django.http      import JsonResponse
from django.views     import View

from orders.models    import OrderStatus, Order, OrderItem
from users.models     import User
from products.models  import Product

from users.utils      import user_decorator

class CartView(View):
    @user_decorator
    def post(self, request):
        try:
            data           = json.loads(request.body)
            user           = request.user
            product        = data['product_id']
            current_amount = 0

            if not Product.objects.filter(id=product).exists():
                return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status=400)

            order, created = Order.objects.get_or_create(
                        user            = user,
                        order_status_id = OrderStatus.PENDING,
                        defaults        = {'order_number':uuid.uuid4()}
                    )

            if OrderItem.objects.filter(order=order, product_id=product).exists():
                current_amount = OrderItem.objects.get(order=order, product_id=product).amount
                
            orderitem, created = OrderItem.objects.update_or_create(
                        order      = order,
                        product_id = product,
                        defaults   = {'amount':data['amount'] + current_amount},
                        )

            return JsonResponse({'message':"SUCCESS", "order_number":order.order_number, "id":orderitem.id},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
