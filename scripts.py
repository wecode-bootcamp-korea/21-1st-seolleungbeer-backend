import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seolleungbeer.settings")
django.setup()

from products.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

CSV_PATH_PRODUCTS='./seolleungbeer_product.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None) # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
    for row in data_reader:

        product_info = ProductInfo.objects.create(
                meterial = row[6],
                size = row[7],
                manufacturer = row[8],
                made = row[9],
                distributor = row[10],
                afterservice = row[11]
        )

        sub_category = SubCategory.objects.get(name=row[1])
        Product.objects.create(korean_name      = row[2],
                                english_name    = row[3],
                                price           = row[4],
                                description     = row[5],
                                sub_category = sub_category,
                                product_info = product_info
        )
        
