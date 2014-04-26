"""
Provides predefine settings for including in your Django project settings
Note: This is not a conventional Django settings.py file, settings 
"""

from doorsale.common import settings as common_settings
from doorsale.catalog import settings as catalog_settings

AUTH_USER_MODEL = 'common.User'

DOORSALE_APPS = (
    'doorsale.geo',
    'doorsale.common',
    'doorsale.catalog',
    'doorsale.sales',
    'doorsale.financial',
)

PIPELINE_CSS = {}
PIPELINE_CSS.update(common_settings.PIPELINE_CSS)
PIPELINE_CSS.update(catalog_settings.PIPELINE_CSS)

PIPELINE_JS =  { }
PIPELINE_JS.update(common_settings.PIPLELINE_JS)
PIPELINE_JS.update(catalog_settings.PIPLELINE_JS)

PIPELINE_COMPILERS = (
  'pipeline.compilers.less.LessCompiler',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_DISABLE_WRAPPER = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'doorsale.common.context_processors.bootstrip',
    'doorsale.catalog.context_processors.bootstrip',
)

