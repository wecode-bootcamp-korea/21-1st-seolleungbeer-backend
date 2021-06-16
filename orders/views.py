import json

from django.views    import View
from django.http     import JsonResponse

from users.utils     import user_decorator
from orders.models   import OrderItem

class CartView(View):
    @user_decorator
    def delete(self, request):
            data       = json.loads(request.body)
            order_item = OrderItem.objects.filter(id__in=data['cart_id'])

            if data['cart_id'] not in order_item:
                return JsonResponse({'message': 'NOT_FOUND'}, status=404)

            order_item.delete()

            rest_value = OrderItem.objects.all()
            rest_value = list(rest_value.values())
            
            return JsonResponse({'message':'DELETE_SUCCESS', 'rest_value':rest_value}, status=200)