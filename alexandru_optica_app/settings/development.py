from pathlib import Path
from .settings import *  # noqa

DEBUG = True

STATIC_ROOT: Path = BASE_DIR / STATIC_URL  # noqa
STATICFILES_DIRS: list[str] = []

ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]  # noqa

LOGGING["handlers"]["console"]["formatter"] = "struct_legacy_color"  # noqa
LOGGING["root"]["level"] = "DEBUG"  # noqa
