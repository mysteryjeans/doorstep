
PIPELINE_CSS = {
    'sales': {
        'source_filenames': (
            'sales/css/sales.less',
        ),
        'output_filename': 'sales/css/sales.css'
    }
}


PIPLELINE_JS = {
    'sales_checkout_order': {
        'source_filenames': (
          'sales/scripts/jquery.creditCardValidator.js',
          'sales/scripts/jquery.checkout_order.js',
        ),
        'output_filename': 'sales/scripts/sales_checkout_order.js',
    }
}