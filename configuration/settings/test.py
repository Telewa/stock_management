from .base import *

CELERY_TASK_ALWAYS_EAGER = (
    True  # without this, celery tests will use prod database !!!!!
)
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
