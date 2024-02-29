from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
import uuid

@receiver(pre_save, sender=Order)
def create_transactions_by_pre_save(sender, instance, **kwargs):
    if instance.transaction_id == "":
        instance.transaction_id = str(uuid.uuid4()).replace("-","").upper()[:10]