from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import PurchaseOrder, Vendor


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor


        completed_orders_count = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed'
        ).count()
        if completed_orders_count > 0:
            on_time_delivery_orders_count = PurchaseOrder.objects.filter(
                vendor=vendor, status='completed', delivery_date__lte=instance.delivery_date
            ).count()
            vendor.on_time_delivery_rate = (on_time_delivery_orders_count / completed_orders_count) * 100
        else:
            vendor.on_time_delivery_rate = 0


        quality_rating_avg = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', quality_rating__isnull=False
        ).aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        vendor.quality_rating_avg = quality_rating_avg or 0

        vendor.save()
