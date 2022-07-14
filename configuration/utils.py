import os


def set_running_environment():
    """
    This function is used only during startup by manage.py and celeryapp
    :return:
    """
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "staging")

    if ENVIRONMENT == "production":
        print("using production settings")
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "configuration.settings.production"
        )
    else:
        print("using staging settings")
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "configuration.settings.staging"
        )
