import os


def set_running_environment():
    """
    This function is used only during startup by manage.py and celeryapp
    :return:
    """
    environment = os.environ.get("ENVIRONMENT", "test")

    print(f"using {environment} settings")
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", f"configuration.settings.{environment}"
    )
