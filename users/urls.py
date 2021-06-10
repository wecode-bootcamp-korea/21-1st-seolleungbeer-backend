from django.urls import path

from .views import SignupView, LoginView, EmailCheckView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/email-check', EmailCheckView.as_view())
]
