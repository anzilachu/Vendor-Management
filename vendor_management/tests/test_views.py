from django.contrib.auth.models import User  # Assuming you have a User model
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from vendor_management.models import Vendor

class VendorViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

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

    def test_vendor_list(self):
        url = reverse("vendor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_vendor_detail(self):
        url = reverse("vendor-detail", args=[self.vendor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Vendor")
