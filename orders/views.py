import json

from django.views     import View
from django.http      import JsonResponse

from users.utils     import user_decorator
from orders.models   import OrderItem, OrderStatus

class CartView(View):
    @user_decorator
    def delete(self, request):
        try:
            data       = json.loads(request.body)
            db_item    = OrderItem.objects.filter(
                order_id=data['order_id'], 
                order__order_status_id = OrderStatus.PENDING
            )
            order_item = OrderItem.objects.filter(id__in=data['cart_item_id'])

            order_item.delete()

            rest_value = db_item.all()
            rest_value = list(rest_value.values())
            
            return JsonResponse({'message':'DELETE_SUCCESS', 'rest_value':rest_value}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'INVAILD_VALUE'}, status=400)