"""
Testing settings for AuShadha project.
Used for automated tests.
"""

from .base import *

# Debug can be True for tests
DEBUG = True

# Allow all hosts in testing
ALLOWED_HOSTS = ['*']

# Use in-memory database for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable password hashing for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable migrations for faster tests (use --no-migrations flag)
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

# MIGRATION_MODULES = DisableMigrations()

# Email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Logging - minimal in tests
LOGGING['root']['level'] = 'ERROR'
LOGGING['loggers']['aushadha']['level'] = 'ERROR'

# Static files - no collection needed
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

print("=" * 80)
print("AUSHADHA 2.0 - TESTING MODE")
print("=" * 80)
