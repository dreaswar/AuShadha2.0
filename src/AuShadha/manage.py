#!/usr/bin/env python
import os
import sys
<<<<<<< HEAD
from django.apps import apps as django_apps
=======
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AuShadha.settings")
    try:
        from django.core.management import execute_from_command_line
<<<<<<< HEAD
        import AuShadha.startup as startup
        print ("Trying to run custom code at startup...")
        print ("Loading apps and roles from configure.yaml")
        #startup.run()
        #print ("Roles for UI loaded")

=======
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
<<<<<<< HEAD
    

=======
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0
