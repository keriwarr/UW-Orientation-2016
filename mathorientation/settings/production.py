import os
from .common import *

# Generate a secret key.
SECRET_KEY = os.environ['SECRET_KEY']
FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET = os.environ['FACEBOOK_APP_SECRET']

# Debug is turned off in production.
DEBUG = False

ENVIRONMENT='production'
