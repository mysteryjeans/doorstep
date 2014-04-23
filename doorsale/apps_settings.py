"""
Provides predefine settings for including in your Django project settings
Note: This is not a conventional Django settings.py file, settings 
"""

AUTH_USER_MODEL = 'common.User'

DOORSALE_APPS = (
    'doorsale.geo',
    'doorsale.common',
    'doorsale.catalog',
    'doorsale.sales',
    'doorsale.financial',
)

PIPELINE_CSS =  { 
    'style': {
        'source_filenames': (
            'css/style.less',
        ),
        'output_filename': 'css/style.css'
    }
}

PIPELINE_JS =  { }
