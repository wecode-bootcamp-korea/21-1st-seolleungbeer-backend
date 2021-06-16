import json

from django.views    import View
from django.http     import JsonResponse

from users.utils     import user_decorator
from orders.models   import OrderItem

class CartView(View):
    @user_decorator
    def delete(self, request):
            data = json.loads(request.body)

            OrderItem.objects.filter(id__in=data['cart_id']).delete()
            
            return JsonResponse({'message':'DELETE_SUCCESS'}, status=200)