
import json,uuid
from copy import deepcopy

from django.http  import JsonResponse
from django.views import View
from django.db.models import F,Q,When,Value,Count

from .models      import Order,OrderItem,OrderStatus
from products.models import Product
from users.utils  import user_decorator


class OrderView(View):
    @user_decorator
    def get(self,request):
        result = {
            request.user.name,
            request.user.email,
            request.user.mobile
        }
        return JsonResponse(result,status=200)

    # @user_decorator
    def post(self,request):
        data = json.loads(request.body)

        # 토큰 유저 정보 = 주문의 유저의 정보 일치하는 지 확인
        if not Order.objects.filter(order_number=data['order_number'], user=request.user).exists():
            return JsonResponse({'message':'Invalid User'}, status=401)

        # 새로운 order 생성(배송메모,최종결제금액,결제방법 저장)
        test = data['order_items'].items()
        [(1,3)(2,2)(3,6)]
        sum = 0
        for i in test:
            sum += i[0]*i[1]

        x = lambda a,b: a+b
        y = lambda c,d: c*d

        reduce(lambda x,y:x+y,test)
        
        new = Order.objects.create(
            order_number = uuid.uuid4(),
            delivery_memo = data['delivery_memo'],
            payment_information = data['payment_information'],
            payment_charge = 'payment_charge',
            user = request.user,
            order_status = 1
        )
        # order item의 FK 값을 새로 생성된 order로 변경
        # order item의 수량을 새로 들어온 수량으로 변경
        # 기존 장바구니 주문에서, 주문된 orderitem의 수량을 빼고 다시 저장(0개가 된 경우 아이템 자체를 삭제)

        for key,value in data['order_item'].items():
            item = OrderItem.objects.get(id=key)

            if item.amount != value:
                item_in_cart = deepcopy(item)
                item_in_cart.update(id=None,amount=F('amount')-value)
                
            item.update(order=new,amount=value)

        OrderItem.objects.filter(id in data['order_item'].keys()).save()                



new_instance = deepcopy(object_you_want_copied)
new_instance.id = None
new_instance.save()



        # 전체에 트랜잭션 처리



#         data['order_number'],
#         data['order_item'],
#         data['delivery_memo'],
#         data['payment_information'],
#         data['payment_charge'],

# 결제 POST request의 body = 
# {
#     order_number: '주문번호(장바구니의 주문번호)',
#     order_item: [아이템.id, 아이템id, 아이템.id, ...],
#     delivery_memo: '배송메모',
#     payment_information: '결제방법',
#     payment_charge: 최종결제금액,
# }
        
