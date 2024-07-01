from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import (CourseViewSet, LessonCreateApiView, LessonListApiView, LessonRetrieveApiView,
                             LessonUpdateApiView, LessonDestroyAPIView, SubscriptionAPIView)

app_name = MaterialsConfig.name
router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListApiView.as_view(), name='lessons_list'),
    path('lessons/<int:pk>/', LessonRetrieveApiView.as_view(), name='lessons_retrieve'),
    path('lessons/create/', LessonCreateApiView.as_view(), name='lessons_create'),
    path('lessons/<int:pk>/update/', LessonUpdateApiView.as_view(), name='lessons_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lessons_delete'),
    path('subscription/create/', SubscriptionAPIView.as_view(), name='subscription_create'),
] + router.urls