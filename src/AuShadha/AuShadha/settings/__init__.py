"""
AuShadha Settings Module
Loads environment-specific settings based on DJANGO_SETTINGS_MODULE
"""

import os

# Default to development if not specified
ENVIRONMENT = os.environ.get('AUSHADHA_ENV', 'development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'testing':
    from .testing import *
else:
    from .development import *
