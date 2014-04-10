"""
Provides predefine settings for including in your Django project settings
Note: This is not a conventional Django settings.py file, settings 
"""

APPS = (
    'doorsale.common',
    'doorsale.catalog',
    'doorsale.sales',
    'doorsale.finance',
)

PIPELINE_CSS =  {
    'doorsale.style': {
        'source_filenames': (
            'doorsale/css/style.less',
            ),
        'output_filename': 'doorsale/css/style.css'
    },
    'doorsale.base': {
        'source_filenames': (
          'doorsale/css/base.less',
        ),
        'output_filename': 'doorsale/css/base.css',        
    },
}