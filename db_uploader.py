import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seolleungbeer.settings")
django.setup()

from products.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

CSV_PATH_PRODUCTS='./seolleungbeer_product.csv'
CSV_PATH_PRODUCTS2='./seolleungbeer_productinfo.csv'
CSV_PATH_PRODUCTS3='./seolleungbeer_product (2).csv'
with open(CSV_PATH_PRODUCTS3) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None) # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
        for row in data_reader:
            product_info = ProductInfo.objects.create(
                        meterial = row[2],
                        size = row[3],
                        manufacturer = row[4],
                        made = row[5],
                        distributor = row[6],
                        afterservice = row[7]
                )
            Product.objects.create(korean_name      = row[2],
                                    english_name    = row[3],
                                    price           = row[4],
                                    description     = row[5],
                                    sub_category_id = sub_category_id,
                                    product_info    = product_info
                                        )
