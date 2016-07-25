#!/usr/bin/env python
import os
import sys
import dotenv

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    dotenv.read_dotenv()

    environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')
    settings = 'mathorientation.settings.{}'.format(environment)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)
    execute_from_command_line(sys.argv)
