from .base import *

DEBUG = True  # ¡Nunca en producción!

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Configuraciones específicas para desarrollo
DATABASES["default"]["NAME"] = BASE_DIR / "db_dev.sqlite3"

# Extras para debug
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # Opcional: restringe acceso
    ],
}

CORS_ALLOW_ALL_ORIGINS = True
