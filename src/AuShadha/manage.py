#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

def load_env():
    """Load environment variables from .env file if it exists"""
    env_file = Path(__file__).resolve().parent.parent.parent / '.env'
    if env_file.exists():
        print(f"Loading environment from: {env_file}")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key, value)
    else:
        print(f"Warning: .env file not found at {env_file}")
        print("Using default/system environment variables")

def main():
    """Run administrative tasks."""
    # Load environment variables first
    load_env()

    # Set default settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuShadha.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
