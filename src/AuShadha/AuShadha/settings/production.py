"""
Production settings for AuShadha project.
SECURITY: Ensure all environment variables are properly set.
"""

from .base import *

# SECURITY: Debug must be False in production
DEBUG = False

# SECURITY: Specify allowed hosts
ALLOWED_HOSTS = get_env('DJANGO_ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError("DJANGO_ALLOWED_HOSTS must be set in production")

# SECURITY: HTTPS Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SECURITY: Proxy settings (if behind nginx/apache)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files - use ManifestStaticFilesStorage for caching
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Email configuration (production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(get_env('EMAIL_PORT', '587'))
EMAIL_USE_TLS = get_env('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = get_env('DEFAULT_FROM_EMAIL', 'noreply@aushadha.org')

# Database - use connection pooling in production
DATABASES['default']['CONN_MAX_AGE'] = 600
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
}

# Logging - production configuration
LOGGING['handlers']['file']['filename'] = '/var/log/aushadha/aushadha.log'
LOGGING['root']['level'] = 'WARNING'
LOGGING['loggers']['aushadha']['level'] = 'INFO'

# Cache configuration (Redis recommended for production)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'aushadha_cache_table',
    }
}

# Session backend (database for production)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Admin security
ADMINS = [
    ('Admin', get_env('ADMIN_EMAIL', 'admin@aushadha.org')),
]

# Error reporting
MANAGERS = ADMINS

print("=" * 80)
print("AUSHADHA 2.0 - PRODUCTION MODE")
print("=" * 80)
print(f"DEBUG: {DEBUG}")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"SECURE_SSL_REDIRECT: {SECURE_SSL_REDIRECT}")
print("=" * 80)
