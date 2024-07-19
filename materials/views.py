from django.utils import timezone
from datetime import *

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from users.permissions import IsModerator, IsOwner
from materials.tasks import send_update_course_mail


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Connect a course with an owner"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_queryset(self):
        """Shows only courses that belong to owner if you are not a moderator"""
        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """Get the permissions"""
        if self.action in ["update", "partial_update", "list", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        if self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()
        course_id = course.id
        course.last_update = datetime.now(timezone.utc)

        send_update_course_mail.delay(course_id)


class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]

    def perform_create(self, serializer):
        """Create a Lesson"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        """Shows only lessons that belong to owner if you are not a moderator"""
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course_item)
        if not created:
            subscription.delete()
            message = 'Subscription removed'
        else:
            message = 'Subscription added'

        return Response({"message": message})

