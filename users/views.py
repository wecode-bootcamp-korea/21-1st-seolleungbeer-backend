import json, re, bcrypt, jwt
from django.http.response import JsonResponse

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError

from .models                import User
from seolleungbeer.settings import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            bcrypt_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            password_regx = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{10,}$")
            email_regex   = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

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
                password = bcrypt_password
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except IntegrityError:
            return JsonResponse({'message': 'INTEGRITY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            input_email    = data['email']
            input_password = data['password'].encode('utf-8')

            if input_email == '' or input_password == '':
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            
            db_email    = User.objects.get(email=input_email)
            db_password = db_email.password.encode('utf-8')

            if not bcrypt.checkpw(input_password, db_password):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
            
            token = jwt.encode({'user_id': db_email.id}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'token': token, 'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class EmailCheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'EMAIL_EXIST'}, status=400)

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)