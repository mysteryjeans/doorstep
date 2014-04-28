

PIPELINE_CSS = {
    'catalog': {
        'source_filenames': (
            'catalog/css/catalog.less',
        ),
        'output_filename': 'catalog/css/catalog.css'
    },
    'font-awesome': {
        'source_filenames': (
            'catalog/css/font-awesome/css/font-awesome.min.css',
        ),
        'output_filename': 'catalog/css/font-awesome/css/font-awesome.min.css'
    }
}

PIPLELINE_JS = {
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
    }
}