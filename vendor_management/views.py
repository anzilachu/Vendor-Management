from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Vendor, PurchaseOrder
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    TokenSerializer,
    UserSerializer,
    VendorPerformanceSerializer,
)


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User registered successfully'},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username, password=password).first()

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserLogoutAPIView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class VendorRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PurchaseOrderListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PurchaseOrderRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.refresh_from_db()
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        # Trigger calculation of metrics when a PO is updated
        instance.vendor.calculate_metrics()


class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        performance_metrics = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': instance.quality_rating_avg,
            'response_time_avg': instance.response_time_avg,
            'fulfillment_rate': instance.fulfillment_rate,
        }

        return Response(performance_metrics)


class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()
        instance.vendor.calculate_metrics()
        return Response(
            {'message': 'Purchase Order acknowledged successfully.'}
        )

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
