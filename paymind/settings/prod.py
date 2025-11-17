from .base import *
import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# ⚠️ Para ponerlo a funcionar YA: aceptamos cualquier host en prod
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}
