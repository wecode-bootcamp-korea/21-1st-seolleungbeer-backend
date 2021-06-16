import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse

from .models                import User
from seolleungbeer.settings import SECRET_KEY, ALGORITHM
from users.utils             import user_decorator

password_regx = re.compile('^.*(?=^.{10,15}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$')
email_regex   = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
mobile_regex  = re.compile('^[0-9]{10,11}$')

class EmailCheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not email_regex.match(data['email']):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)
                
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'EMAIL_EXIST'}, status=400)

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class MobileCheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not mobile_regex.match(data['mobile']):
                return JsonResponse({'message': 'INVALID_MOBILE'}, status=400)
           
            if User.objects.filter(mobile = data['mobile']).exists():
                return JsonResponse({'message': 'MOBILE_EXIST'}, status=400)

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

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

class AccountInfoView(View):
    @user_decorator
    def get(self,request):
        result = {
            'name': request.user.name,
            'email': request.user.email,
            'mobile': request.user.mobile
        }
        return JsonResponse(result,status=200)