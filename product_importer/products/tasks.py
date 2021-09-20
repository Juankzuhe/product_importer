import time

from celery import shared_task

from celery_progress.backend import ProgressRecorder
from .models import Product



@shared_task(bind=True)
def import_products(self, dataset):
    progress_recorder = ProgressRecorder(self)
    for index, product in enumerate(dataset):
        time.sleep(0.3)
        Product.objects.update_or_create(
            sku=product.get("sku").lower(),
            defaults={
                "name": product.get("name"),
                "sku": product.get("sku").lower(),
                "description": product.get("description"),
                "is_active": product.get("is_active"),
            }
        )
        progress_recorder.set_progress(index + 1, len(dataset))
