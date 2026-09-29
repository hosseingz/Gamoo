import environ
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Register custom apps directory so modules inside apps/ can be referenced without prefix
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Initialize environment parser using django-environ
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ""),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1", "django-app"]),
    CORS_ALLOWED_ORIGINS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
)

# Read environment variables from .env file if present
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

# Parse clean lists of allowed hosts
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
for fallback_host in ['localhost', '127.0.0.1', 'django-app']:
    if fallback_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(fallback_host)

ENVIRONMENT = env('DJANGO_ENV', default='production').lower().strip()
DOMAIN = env('DOMAIN', default='localhost')

# Parse CORS/CSRF configurations from environment variables
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# If lists are empty, apply standard domain fallbacks
if not CORS_ALLOWED_ORIGINS and DOMAIN:
    CORS_ALLOWED_ORIGINS = [f"http://{DOMAIN}", f"https://{DOMAIN}"]
if not CSRF_TRUSTED_ORIGINS and DOMAIN:
    CSRF_TRUSTED_ORIGINS = [f"http://{DOMAIN}", f"https://{DOMAIN}"]

# Expand standard local addresses for development or testing
if ENVIRONMENT in ["development", "local"]:
    local_origins = [
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    for origin in local_origins:
        if origin not in CORS_ALLOWED_ORIGINS:
            CORS_ALLOWED_ORIGINS.append(origin)
        if origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(origin)

CORS_ALLOW_CREDENTIALS = True

# Secure Proxy Configuration for Nginx reverse proxy setups
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'corsheaders',
    'rest_framework',
    'blog',
]

# Optimized middleware hierarchy (WhiteNoise positioned directly under SecurityMiddleware)
MIDDLEWARE = [
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Intercept and serve static files directly
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Unified database connections using 12-factor-friendly DATABASE_URL
postgres_fallback = f"postgres://{env('POSTGRES_USER', default='postgres')}:{env('POSTGRES_PASSWORD', default='postgres')}@{env('POSTGRES_HOST', default='database')}:{env('POSTGRES_PORT', default='5432')}/{env('POSTGRES_DB', default='postgres')}"
DATABASES = {
    'default': env.db('DATABASE_URL', default=postgres_fallback)
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = ""
LOGOUT_REDIRECT_URL = LOGIN_URL

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Prevent startup failure if the local assets folder does not exist
STATICFILES_DIRS = []
assets_dir = BASE_DIR / "assets"
if assets_dir.exists():
    STATICFILES_DIRS.append(assets_dir)
