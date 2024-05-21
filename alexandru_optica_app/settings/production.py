from .settings import *  # noqa

LANGUAGE_CODE = "ro"

ALLOWED_HOSTS = ["alexandru-optica.alwaysdata.net"]

STATIC_ROOT = BASE_DIR / "static/"  # noqa

LOGGING["handlers"]["console"]["formatter"] = "struct_json"  # noqa
