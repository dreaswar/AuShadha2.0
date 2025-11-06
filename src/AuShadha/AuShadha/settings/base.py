"""
Base Django settings for AuShadha project.
Common settings shared across all environments.
"""

import os
import sys
import yaml
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_PATH = Path(__file__).resolve().parent.parent
PARENT_ROOT = ROOT_PATH.parent

# Environment variable helper
def get_env(key, default=None, required=False):
    """Get environment variable with optional default and required check"""
    value = os.environ.get(key, default)
    if required and value is None:
        raise ValueError(f"Environment variable '{key}' is required but not set")
    return value

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env('DJANGO_SECRET_KEY', required=True)

# Application URLs
APP_ROOT_URL = get_env('APP_ROOT_URL', '/AuShadha/')
LOGIN_URL = APP_ROOT_URL + 'authenticate/login/'
LOGIN_REDIRECT_URL = APP_ROOT_URL

# Serialization
SERIALIZATION_MODULES = {
    'yml': "django.core.serializers.pyyaml"
}

# Admins and Managers
ADMINS = [
    ('Dr.Easwar T.R', 'dreaswar@gmail.com'),
]
MANAGERS = ADMINS

# Custom User Model (uncomment when ready)
# AUTH_USER_MODEL = 'aushadha_users.AuShadhaUser'

# Application definition
INSTALLED_APPS = [
    # Django Core Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',

    # AuShadha Core Apps
    'aushadha_ui.apps.AushadhaUiConfig',
    'aushadha_base_models.apps.AushadhaBaseModelsConfig',
    'aushadha_users.apps.AushadhaUsersConfig',
    'clinic.apps.ClinicConfig',
    'search',
    'patient.apps.PatientConfig',

    # Medical Registries
    'registry.icd10',
    'registry.icd10pcs',
    'registry.drug_db',
    'registry.drug_db.drugbankca',
    'registry.inv_and_imaging',
    'registry.vaccine_registry',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AuShadha.urls'

SITE_ID = 1

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'static',
            BASE_DIR / 'aushadha_ui' / 'static',
            BASE_DIR / 'aushadha_users' / 'static',
        ],
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

WSGI_APPLICATION = 'AuShadha.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DB_ENGINE = get_env('DB_ENGINE', 'django.db.backends.postgresql_psycopg2')
DB_CONFIG = {
    'ENGINE': DB_ENGINE,
    'NAME': get_env('DB_NAME', required=True),
}

# PostgreSQL/MySQL specific settings (not needed for SQLite)
if 'sqlite' not in DB_ENGINE:
    DB_CONFIG.update({
        'USER': get_env('DB_USER', required=True),
        'PASSWORD': get_env('DB_PASSWORD', required=True),
        'HOST': get_env('DB_HOST', 'localhost'),
        'PORT': get_env('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling
    })

DATABASES = {'default': DB_CONFIG}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = get_env('TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security Settings
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Session Settings
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True

# Ensure logs directory exists
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'aushadha.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'aushadha': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Load enabled apps from YAML configuration (SECURE VERSION)
try:
    config_path = ROOT_PATH / 'configure.yaml'
    if config_path.exists():
        with open(config_path, 'r') as f:
            # SECURITY FIX: Use safe_load instead of load
            config = yaml.safe_load(f)
            ENABLED_APPS = config if config else list(INSTALLED_APPS)
    else:
        ENABLED_APPS = list(INSTALLED_APPS)
except Exception as e:
    # Log error but don't crash
    print(f"Warning: Could not load configure.yaml: {e}")
    ENABLED_APPS = list(INSTALLED_APPS)

# AuShadha specific settings
UI_INITIALIZED = False
