# flake8: noqa
# type: ignore
try:
    import oiq.auth_db.models
    from django.apps import apps
    from oiq.auth_db.core import _generate_secret_key
    from oiq.email_db import models
    from oiq.user_db import interface as user_db
    from oiq.user_db.interface import _get_user_model
    from oiq.user_db.models import User

    apps.get_model("core", "Comment")
except ImportError:
    pass
