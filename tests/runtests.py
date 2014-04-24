#!/usr/bin/env python
import os
import sys

from optparse import OptionParser
from doorsale import settings


if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--settings', dest='settings', type='string', help='name of the django settings')

    (options, args) = parser.parse_args()

    if options.settings is None:
        parser.error('You must supply django settings')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", options.settings)

    from django.core.management import call_command

    call_command('test', *settings.DOORSALE_APPS)
