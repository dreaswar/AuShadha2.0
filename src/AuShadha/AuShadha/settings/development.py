"""
Development settings for AuShadha project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# Development database (can use SQLite for quick testing)
# Uncomment to use SQLite instead of PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Django Debug Toolbar (optional - install if needed)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INTERNAL_IPS = ['127.0.0.1']

# Disable HTTPS-only cookies in development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email backend for development (console output)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files - no caching in development
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Logging - more verbose in development
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['aushadha']['level'] = 'DEBUG'

# Performance - disable template caching
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

print("=" * 80)
print("AUSHADHA 2.0 - DEVELOPMENT MODE")
print("=" * 80)
print(f"DEBUG: {DEBUG}")
print(f"DATABASE: {DATABASES['default']['ENGINE']}")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print("=" * 80)
