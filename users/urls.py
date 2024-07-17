from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView, PaymentCreateAPIView

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payment/create", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("login/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="login",),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="token_refresh",),
] + router.urls