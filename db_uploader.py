import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seolleungbeer.settings")
django.setup()

from products.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

CSV_PATH_PRODUCTS='./product.csv'
# CSV_PATH_PRODUCTS='./product_image.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None) # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함

# #         # 이미지 상품 이미지할때 사용 !!!!주의:이미지타입 main,list가 저장 되어있어야함 !
#         for row in data_reader:
#             product_name= row[0]
#             type=row[3]

#             ProductImage.objects.create(
#                 image_url=row[1],
#                 image_type_id = ImageType.objects.get(type=type).id,
#                 product_id = Product.objects.get(korean_name=product_name).id
#             )


        #  상품, 상품인포 할때사용
        for row in data_reader:
            sub_category_name =row[0]
            product_info = ProductInfo.objects.create(
                        meterial = row[5],
                        size = row[6],
                        manufacturer = row[7],
                        made = row[8],
                        distributor = row[9],
                        afterservice = row[10]
                )
            Product.objects.create(korean_name      = row[1],
                                    english_name    = row[2],
                                    price           = row[3],
                                    description     = row[4],
                                    sub_category_id = SubCategory.objects.get(korean_name=sub_category_name).id,
                                    product_info    = product_info,
                                    main_image      = row[11]
        )
