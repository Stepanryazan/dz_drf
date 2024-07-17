from django.contrib import admin

from materials.models import Lesson, Course, Subscription

admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(Subscription)