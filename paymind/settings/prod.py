from .base import *
import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = ["paymind.onrender.com"]

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# Archivos estáticos en producción
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []   # ← MUY IMPORTANTE: vacío en producción

# WhiteNoise para servir archivos estáticos en producción
# Debe ir DESPUÉS de SecurityMiddleware pero ANTES de otros middlewares
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuración de WhiteNoise
# Usamos CompressedStaticFilesStorage (sin manifest) porque django-tailwind
# genera nombres fijos sin hash
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
