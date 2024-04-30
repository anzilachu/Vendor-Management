from django.test import TestCase
from vendor_management.models import Vendor, PurchaseOrder, HistoricalPerformance
from datetime import datetime 


class VendorModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact",
            address="Address",
            vendor_code="V001",
            on_time_delivery_rate=80,
            quality_rating_avg=4,
            average_response_time=2,
            fulfillment_rate=90
        )

    def test_vendor_str(self):
        self.assertEqual(str(self.vendor), "Test Vendor")

class PurchaseOrderModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact",
            address="Address",
            vendor_code="V001",
            on_time_delivery_rate=80,
            quality_rating_avg=4,
            average_response_time=2,
            fulfillment_rate=90
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date="2024-04-30T12:00:00Z",
            delivery_date="2024-05-10T12:00:00Z",
            items={"item1": 10, "item2": 5},
            quantity=15,
            status="completed",
            quality_rating=4.5
        )

    def test_purchase_order_str(self):
        self.assertEqual(str(self.purchase_order), "PO001")  # This assertion is failing


class HistoricalPerformanceModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact",
            address="Address",
            vendor_code="V001",
            on_time_delivery_rate=80,
            quality_rating_avg=4,
            average_response_time=2,
            fulfillment_rate=90
        )
        self.performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date=datetime(2024, 4, 30, 12, 0, 0),  # Use datetime without the redundant .datetime
            on_time_delivery_rate=85,
            quality_rating_avg=4.2,
            average_response_time=2.1,
            fulfillment_rate=88
        )

    def test_performance_str(self):
        expected_str = f"{self.vendor.name} - 2024-04-30T12:00:00Z"  # Manually construct the expected string
        actual_str = str(self.performance)
        self.assertEqual(actual_str, expected_str)



class PurchaseOrderModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact",
            address="Address",
            vendor_code="V001",
            on_time_delivery_rate=80,
            quality_rating_avg=4,
            average_response_time=2,
            fulfillment_rate=90
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date="2024-04-30T12:00:00Z",
            delivery_date="2024-05-10T12:00:00Z",
            items={"item1": 10, "item2": 5},
            quantity=15,
            status="completed",
            quality_rating=4.5
        )

    def test_purchase_order_str(self):
        self.assertEqual(str(self.purchase_order), "PO001")

