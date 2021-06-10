import json, re
from django.http.response import JsonResponse

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError

from .models      import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            password_regx = re.compile('^.*(?=^.{10,15}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$')
            email_regex   = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'EMAIL_EXIST'}, status=400)

            if User.objects.filter(mobile = data['mobile']).exists():
                return JsonResponse({'message': 'MOBILE_EXIST'}, status=400)

            if not email_regex.match(data['email']):
                return JsonResponse({'message':'PLEASE ENTER @ OR .'}, status=400)

            if not password_regx.match(data['password']):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

            User.objects.create(
                sex      = data['sex'],
                name     = data['name'],
                email    = data['email'],
                mobile   = data['mobile'],
                password = data['password']
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except IntegrityError:
            return JsonResponse({'message': 'INTEGRITY_ERROR'}, status=400) 