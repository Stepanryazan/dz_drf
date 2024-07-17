import pytz
from datetime import *

from celery import shared_task

from config import settings
from users.models import User


@shared_task
def check_last_login():
    """Blocks the user if he has not logged in for more than 30 days"""
    users = User.objects.filter(is_active=True)
    for user in users:
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()