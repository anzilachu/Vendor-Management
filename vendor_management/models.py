from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    quality_rating_avg = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def calculate_metrics(self):
    
        completed_orders = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)

        completed_orders_count = completed_orders.count()
        if completed_orders_count > 0:
            on_time_delivery_orders_count = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
            self.on_time_delivery_rate = (on_time_delivery_orders_count / completed_orders_count) * 100
        else:
            self.on_time_delivery_rate = 0

        quality_rating_avg = completed_orders.aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating']
        self.quality_rating_avg = quality_rating_avg or 0

        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=models.ExpressionWrapper(models.F('acknowledgment_date') - models.F('issue_date'),
                                                   output_field=models.DurationField())
        )
        response_time_avg = response_times.aggregate(avg_response=models.Avg('response_time'))['avg_response']
        self.response_time_avg = response_time_avg.total_seconds() if response_time_avg else 0

        fulfilled_orders_count = completed_orders.count()
        if fulfilled_orders_count > 0:
            self.fulfillment_rate = (fulfilled_orders_count / completed_orders_count) * 100
        else:
            self.fulfillment_rate = 0

        self.save()
    
    def __str__(self):
        return self.name



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])
    quality_rating = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class CustomToken(models.Model):
    token = models.OneToOneField(Token, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
