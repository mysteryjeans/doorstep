
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


################## Doorsale #########################
#####################################################

# Doorsale e-commerce settings for Django project
# Customize these settings only if you know

# Django authentication app extended by Doorsale in Django way
# To implement your own custom auth user model, extend
# doorsale.accounts.AbstractUser instead and change AUTH_USER_MODEL
# similarly. Doorsale will adopt new AUTH_USER_MODEL seemlessly
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# Doorsale apps configuration required for Django
INSTALLED_APPS += (
    'doorsale',
    'doorsale.geo',
    'doorsale.pages',
    'doorsale.accounts',
    'doorsale.catalog',
    'doorsale.sales',
    'doorsale.financial',
    'doorsale.payments',
)

# Thumbnail generator app for Doorsale
INSTALLED_APPS += (
    'easy_thumbnails',
)

################ Django-Pipeline #####################
######################################################

# Doorsale uses django-pipeline for LESS & Javascript
# preprocessing, compression and versioning.

# When collectstatic called during deployment LESS & Javascript will be
# compiled, compressed and versioned before copying to static folder

# Django-Pipeline app required by Doorsale
INSTALLED_APPS += ('pipeline',)

# LESS compiler configuration for django-pipeline
PIPELINE_COMPILERS = ('pipeline.compilers.less.LessCompiler',)

# LESS & Javascript static files serving in development
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

# Pipeline finders for serving pipeline static files
from django.conf.global_settings import STATICFILES_FINDERS
STATICFILES_FINDERS += (
    'pipeline.finders.PipelineFinder',
)

# Custom Javascript needs to be in global scope
# in order for Doorsale to work properly
PIPELINE_DISABLE_WRAPPER = True

# LESS compiler search paths for resources
# Always use relative paths in @import statements in LESS
# All resources in app's static directory will be available
# for LESS compiler
from doorsale.utils.finders import get_static_paths
STATIC_PATHS = os.pathsep.join(get_static_paths(INSTALLED_APPS))
PIPELINE_LESS_ARGUMENTS = '--include-path="%s"' % STATIC_PATHS

# CSS configurations for django-pipeline
# All LESS styles configured for doorsale defined
# You can append your LESS configurations here.
PIPELINE_CSS = {
    # doorsale app LESS styles
    'base': {
        'source_filenames': (
            'doorsale/css/base.less',
        ),
        'output_filename': 'doorsale/css/base.css'
    },
    # doorsale.catalog LESS styles for products catalog
    'catalog': {
        'source_filenames': (
            'catalog/css/catalog.less',
        ),
        'output_filename': 'catalog/css/catalog.css'
    },
    # Font-Awesome icons serve mostly
    'font-awesome': {
        'source_filenames': (
            'catalog/css/font-awesome/css/font-awesome.min.css',
        ),
        'output_filename': 'catalog/css/font-awesome/css/font-awesome.min.css'
    },
    # doorsale.sales LESS styles for checkout pages
    'sales': {
        'source_filenames': (
            'sales/css/sales.less',
        ),
        'output_filename': 'sales/css/sales.css'
    },
    # doorsale.pages LESS styles for flat pages
    'pages': {
        'source_filenames': (
            'pages/css/pages.less',
        ),
        'output_filename': 'pages/css/pages.css'
    }
}


# Javascript configuration for django-pipeline
# Doorsale app's Javascript compressed & versioned before deployment
# Simply add your project or apps Javascript here
PIPELINE_JS = {
    # doorsale: Base javascript include in every page
    'base': {
        'source_filenames': (
            'doorsale/scripts/jquery-ajax.js',
            'doorsale/scripts/jquery-utils.js',
        ),
        'output_filename': 'doorsale/scripts/base.js',
    },
    # doorsale.catalog: Javascript for product catalog pages
    'catalog_base': {
        'source_filenames': (
            'catalog/scripts/jquery.catalog_base.js',
        ),
        'output_filename': 'catalog/scripts/catalog_base.js',
    },
    'search_products': {
        'source_filenames': (
            'catalog/scripts/jquery.search_products.js',
        ),
        'output_filename': 'catalog/scripts/search_products.js',
    },
    'product_detail': {
        'source_filenames': (
            'catalog/scripts/jquery.scrollTo.js',
            'catalog/scripts/jquery.serialScroll.js',
            'catalog/scripts/jquery.elevatezoom.js',
            'catalog/scripts/jquery.product_detail.js',
        ),
        'output_filename': 'catalog/scripts/product_detail.js',
    },
    'sales_checkout_order': {
        'source_filenames': (
            'sales/scripts/jquery.creditCardValidator.js',
            'sales/scripts/jquery.maskedinput.js',
            'sales/scripts/jquery.checkout_order.js',
        ),
        'output_filename': 'sales/scripts/sales_checkout_order.js',
    }
}

# Views to render page from doorsale.pages
PAGE_VIEWS = (('pages_base_page', 'Base View'),
              ('pages_catalog_page', 'Catalog View')
)
