from django.shortcuts import render

# Create your views here.
import json
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q 
from orders.models    import OrderStatus, Order, OrderItem
from users.models     import User
from products.models  import Product
from users.utils      import user_decorator

class CartView(View):
    @user_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user           = request.user
            order_status   = OrderStatus.objects.get(status="장바구니")
            product        = Product.objects.get(korean_name=data['korean_name'])
            current_amount = 0
            if not Order.objects.filter(order_number=data['order_number']).exists():
                current_charge = 0
            else:
                current_charge = int(float((Order.objects.get(order_number=data['order_number']).payment_charge)))
            Order.objects.update_or_create(
                order_number        = data['order_number'],
                delivery_charge     = data['delivery_charge'],
                delivery_method     = data['delivery_method'],
                delivery_memo       = data['delivery_memo'],
                payment_information = data['payment_information'],
                defaults            = {'payment_charge': product.price*data['amount']+current_charge},
                user                = user,
                order_status        = order_status
            )
            order = Order.objects.get(order_number=data['order_number'])
            if OrderItem.objects.filter(Q(order=order) & Q(product=product)):
                current_amount = OrderItem.objects.get(order=order, product = product).amount
            OrderItem.objects.update_or_create(
                order    = order,
                product  = product,
                defaults = {'amount':data['amount'] + current_amount},
                )
            return JsonResponse({'message':"SUCCESS"},status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message':'UNREGISTERED_PRODUCT'}, status=400)
    @user_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            order_status   = OrderStatus.objects.get(status="장바구니")
            product        = Product.objects.get(korean_name=data['korean_name'])
            order = Order.objects.get(user=user,order_status=order_status)
            order.orderitem_set.filter(order=order,product=product).update(amount=data['amount'])
            return JsonResponse({'message':'수량변경성공'},status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)