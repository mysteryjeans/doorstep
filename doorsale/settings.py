"""
Provides predefine settings for including in your Django project settings
Note: This is not a conventional Django settings.py file, settings 
"""

import os


from doorsale.catalog import settings as catalog_settings
from doorsale.sales import settings as sales_settings


DOORSALE_DIR = os.path.dirname(__file__)


# Use Doorsale accounts.User as auth user model
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# All doorsale apps
DOORSALE_APPS = (
    'doorsale',
    'doorsale.geo',
    'doorsale.accounts',
    'doorsale.catalog',
    'doorsale.sales',
    'doorsale.financial',
)

# CSS settings for django-pipeline app
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'doorsale/css/base.less',
        ),
        'output_filename': 'doorsale/css/base.css'
    }
}
PIPELINE_CSS.update(catalog_settings.PIPELINE_CSS)
PIPELINE_CSS.update(sales_settings.PIPELINE_CSS)

# Javascript settings for django pipeline
PIPELINE_JS = {
    'base': {
        'source_filenames': (
          'doorsale/scripts/jquery-ajax.js',
          'doorsale/scripts/jquery-utils.js',
        ),
        'output_filename': 'doorsale/scripts/base.js',
    },
}
PIPELINE_JS.update(catalog_settings.PIPLELINE_JS)

# Doorsale settings to use Less compiler when collectstatic called
PIPELINE_COMPILERS = (
  'pipeline.compilers.less.LessCompiler',
)

# Required to serve static files
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Allow Javascript functions to global scope
PIPELINE_DISABLE_WRAPPER = True

