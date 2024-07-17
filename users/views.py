from datetime import datetime

import pytz
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from config import settings
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Hashes the password and makes the user active"""
        user = serializer.save(is_active=True)
        user.last_login = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        """Allow any user (authenticated or not) to perform create action"""
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, payment_method="Безналичный расчет")
        product = create_stripe_product(payment.paid_course)
        price = create_stripe_price(product=product, payment_amount=payment.payment_amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()