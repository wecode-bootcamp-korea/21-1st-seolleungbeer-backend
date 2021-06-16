
import json,uuid
from copy import deepcopy

from django.http  import JsonResponse
from django.views import View
from django.db.models import F,Q,When,Value,Count

from .models      import Order,OrderItem,OrderStatus
from products.models import Product
from users.models import User
from users.utils  import user_decorator


class OrderView(View):
    @user_decorator
    def get(self,request):
        result = {
            'name': request.user.name,
            'email': request.user.email,
            'mobile': request.user.mobile
        }
        return JsonResponse(result,status=200)

    # @user_decorator
    def post(self,request):
        data = json.loads(request.body)
        print(data)
        new_order = Order.objects.create(
            order_number = uuid.uuid4(),
            delivery_memo = data['delivery_memo'],
            payment_information = data['payment_information'],
            user = User.objects.get(name="앤"),
            order_status_id = 1,
        )

        sum = 0

        # 장바구니 등록을 거쳐서 오는 경우
        for key,value in data['order_item'].items():
            item = OrderItem.objects.filter(id=key).first()

            if item.amount != value:
                item_in_cart = deepcopy(item)
                item_in_cart.update(id=None,amount=F('amount')-value)
                
            item.update(order=new_order,amount=value)
            sum += item.amount * item.product.price

        # # 상품 상세 바로 결제 / 장바구니에서 결제가 나뉘는 경우 (프런트에서 각각 Product ID의 값과 OrderItem의 값을 받는 경우)
        # if data['product_id']:
        #     for key,value in data['order_item'].items():
        #         OrderItem.objects.filter(id=key).update(order=new_order)

        # else:
        #     OrderItem.objects.create(
        #         product__id=key, order=new_order, amount=value
            # )


        if sum != data['payment_information']:
            return JsonResponse({'message':'PAYMENT CHARGE ERROR'}, status=401)

        new_order.payment_information = sum
        new_order.save()

        return JsonResponse({'message':'SUCCESS'}, status=200)