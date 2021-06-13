from django.urls import path

from .views      import SignupView, LoginView, EmailCheckView, MobileCheckView 

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/email-check', EmailCheckView.as_view()),
    path('/mobile-check', MobileCheckView.as_view()),
] 