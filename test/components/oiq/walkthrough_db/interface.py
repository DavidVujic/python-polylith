# flake8: noqa
# type: ignore
try:
    import oiq.walkthrough_db.models as models
    from oiq.walkthrough_db.core import _walkthrough_image
    from oiq.walkthrough_db.models import Walkthrough
except ImportError:
    pass
