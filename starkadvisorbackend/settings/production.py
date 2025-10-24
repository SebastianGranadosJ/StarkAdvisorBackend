from .base import *      # noqa
import os

# =========================
# Flags de seguridad
# =========================
DEBUG = env.bool("DEBUG", default=False)

# Asegúrate de definir ALLOWED_HOSTS en Azure (separado por comas si usas env.list)
# Ej: starkadvisor-backend-XXXX.azurewebsites.net
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["tudominio.com", "www.tudominio.com"])
print(f"🚀 ALLOWED_HOSTS en producción: {ALLOWED_HOSTS}")

SECRET_KEY = env("SECRET_KEY")

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# (Opcional recomendado) HSTS en producción
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# =========================
# Base de Datos (PostgreSQL Azure)
# =========================
# Tu production.py usa variables DB_*, no DATABASE_URL.
# En Azure define:
#   DB_NAME=starkadvisor_db
#   DB_USER=juancknino123
#   DB_PASSWORD=****
#   DB_HOST=starkadvisor-backend-db.postgres.database.azure.com
#   DB_PORT=5432
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="starkadvisorbd"),
        "USER": env("DB_USER", default="postgres"),
        "PASSWORD": env("DB_PASSWORD", default="Kmus.422_pg"),
        "HOST": env("DB_HOST", default="starkadvisorbd.cijmgq2847dz.us-east-1.rds.amazonaws.com"),
        "PORT": env("DB_PORT", default="5432"), 
        # Fuerza SSL con Azure PostgreSQL
        "OPTIONS": {
            "sslmode": "require",
        },
        # (Opcional) Pooling básico
        # "CONN_MAX_AGE": 600,
    }
}

# =========================
# Redis (opcional)
# =========================
REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
REDIS_KEY_PREFIX = env("REDIS_KEY_PREFIX", default="starkadvisor_prod")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "SOCKET_CONNECT_TIMEOUT": 5,
            # "SOCKET_TIMEOUT": 5,
        },
        "KEY_PREFIX": REDIS_KEY_PREFIX,
    }
}

# =========================
# Archivos estáticos / media
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# =========================
# Logging
# =========================
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "django_errors.log"),
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
