import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse

from .models                import User
from seolleungbeer.settings import SECRET_KEY, ALGORITHM

password_regx = re.compile('^.*(?=^.{10,15}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$')

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            bcrypt_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            if not password_regx.match(data['password']):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
            
            User.objects.create(
                sex      = data['sex'],
                name     = data['name'],
                email    = data['email'],
                mobile   = data['mobile'],
                password = bcrypt_password
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            input_email    = data['email']
            input_password = data['password'].encode('utf-8')

            if not User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=400)
            
            db_email       = User.objects.get(email=input_email)
            db_password = db_email.password.encode('utf-8')

            if not bcrypt.checkpw(input_password, db_password):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            
            access_token = jwt.encode({'user_id': db_email.id}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'token': access_token, 'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)