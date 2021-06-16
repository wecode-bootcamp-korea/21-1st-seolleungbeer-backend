import json, uuid

from json.decoder    import JSONDecodeError

from django.http      import JsonResponse
from django.views     import View

from orders.models   import OrderStatus, Order, OrderItem
from products.models import Product
from users.utils     import user_decorator

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

            order, is_created = Order.objects.get_or_create(
                        user            = user,
                        order_status_id = OrderStatus.PENDING,
                        defaults        = {'order_number':uuid.uuid4()}
                    )

            if OrderItem.objects.filter(order=order, product_id=product).exists():
                current_amount = OrderItem.objects.get(order=order, product_id=product).amount

            order_item, is_created = OrderItem.objects.update_or_create(
                        order      = order,
                        product_id = product,
                        defaults   = {'amount':data['amount'] + current_amount},
                        )

            return JsonResponse({'message':"SUCCESS", "order_item_id":order_item.id},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

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
    def patch(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            product = data['product_id']

            if not Product.objects.filter(id=product).exists():
                return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status=404)

            if not OrderItem.objects.filter(order__user=user, product=product, order__order_status_id = OrderStatus.PENDING).exists():
                return JsonResponse({'message':"PRODUCT_DOES_NOT_MATCH"},status=404)

            order_item = OrderItem.objects.get(order__user=user, order__order_status_id=OrderStatus.PENDING, product_id=product)
            order_item.amount=data['amount']
            order_item.save()

            return JsonResponse({'message':'CHANGE SUCCESS',"order_itme_id":order_item.id},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)



    def put(self, request):
        try:
            data       = json.loads(request.body)
            order_item = OrderItem.objects.filter(id__in=data['cart_item_id'])

            order_item.delete()
            
            return JsonResponse({'message':'DELETE_SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'INVAILD_VALUE'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
