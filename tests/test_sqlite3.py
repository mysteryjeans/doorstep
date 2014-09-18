# Test settings for using sqlite3 database
from base_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    },
}
