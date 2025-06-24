from .base import *

DEBUG = True  # ¡Nunca en producción!

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Configuraciones específicas para desarrollo
DATABASES["default"]["NAME"] = BASE_DIR / "db_dev.sqlite3"

# Extras para debug
INSTALLED_APPS += ["debug_toolbar", "rest_framework.authtoken"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
