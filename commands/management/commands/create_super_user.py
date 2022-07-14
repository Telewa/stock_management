from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management import BaseCommand
import os

from structlog import getLogger

logger = getLogger(__file__)


class Command(BaseCommand):
    """
    Run this command when you want manually update the Image colors for all the BackgroundImage in existance
    This is not done in a migration because it is:
    1. Slow
    2. Can be re run (re used) just ok
    """

    def handle(self, *args, **kwargs):
        # only doing this for background images only. Card images will be done next
        user, created = User.objects.get_or_create(
            email=os.environ.get("SUPER_USER_EMAIL"),
            defaults=dict(
                username=os.environ.get("SUPER_USERNAME"),
                is_staff=True,
                is_superuser=True,
                password=make_password(os.environ.get("SUPER_PASSWORD")),
                is_active=True,
            ),
        )

        logger.info(f"{user.email} has been {'created' if created else 'found'}")
