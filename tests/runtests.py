#!/usr/bin/env python
import os


from optparse import OptionParser

DOORSALE_APPS = (
    'doorsale',
    'doorsale.geo',
    'doorsale.pages',
    'doorsale.accounts',
    'doorsale.catalog',
    'doorsale.sales',
    'doorsale.financial',
    'doorsale.payments',
)


if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--settings', dest='settings', type='string', help='name of the django settings')

    (options, args) = parser.parse_args()

    if options.settings is None:
        parser.error('You must supply django settings')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", options.settings)

    from django.core.management import call_command

    call_command('test', *DOORSALE_APPS)
