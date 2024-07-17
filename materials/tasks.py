import pytz
from datetime import *

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Subscription


@shared_task
def send_update_course_mail(course_id):
    """
    Sends email to subscribers if course wasn't updated more than 4 hours ago.
    """
    subscriptions = Subscription.objects.filter(course_id=course_id, status=True)
    for subscription in subscriptions:
        if (subscription.status
                and subscription.course.last_update < datetime.now(pytz.timezone(settings.TIME_ZONE))
                + timedelta(hours=4)):
            send_mail(
                subject=f"Курс '{subscription.course.name}' был обновлен.",
                message=f"В программе курса '{subscription.course.name}' произошли изменения.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
            )