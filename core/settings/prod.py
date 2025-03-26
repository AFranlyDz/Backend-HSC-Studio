from .base import *
#import dj_database_url

DEBUG = False

#ALLOWED_HOSTS = ['api.midominio.com']

# Base de datos en producción (PostgreSQL)
# DATABASES = {
#     'default': dj_database_url.config(conn_max_age=600, default=os.getenv('DATABASE_URL'))
# }

# Seguridad
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

#CORS_ALLOWED_ORIGINS = ['https://tufrontend.com']