import json, re

from django.views import View
from django.http  import JsonResponse

from .models import Order

class CartGetView(View):
    @
    def get