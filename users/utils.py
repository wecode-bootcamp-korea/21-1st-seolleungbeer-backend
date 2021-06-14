import jwt

from django.http            import JsonResponse

from .models                import User
from seolleungbeer.settings import SECRET_KEY, ALGORITHM

def user_decorator(func):
    def wrapper(self, request):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id=payload['user_id'])
            request.user = user

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        return func(self, request)

    return wrapper