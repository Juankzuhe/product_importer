import json

from config import celery_app

from .models import Product


@celery_app.task(serializer="json")
def import_products(dataset):
    dataset = json.loads(dataset)
    batch_size = 1000
    total_products = len(dataset)
    objs = [
        Product(
            name=product["name"],
            sku=product["sku"],
            description=product["description"],
            is_active=product["is_active"],
        )
        for product in dataset
    ]

    products = [objs[i : i + batch_size] for i in range(0, total_products, batch_size)]
    for product in products:
        Product.objects.bulk_create(product, batch_size=1000, ignore_conflicts=True)
