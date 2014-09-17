import os
import sys

from setuptools import setup, find_packages


EXCLUDE_FROM_PACKAGES = ['doorsale.conf.project_settings',
                         'doorsale.bin']

# Dynamically calculate the version based on django.VERSION.
version = __import__('doorsale').get_version()


SETUP_DIR = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(SETUP_DIR, 'README.md')) as readme:
    README = readme.read()

# Allowing setup to run from any location
os.chdir(SETUP_DIR)


setup(name='Doorsale',
      version=version,
      url='https://github.com/mysteryjeans/doorsale',
      author='Faraz Masood Khan',
      author_email='faraz@fanaticlab.com',
      description='The powerful e-commerce solution for Django.',
      long_description=README,
      license='GPLv2',
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
      include_package_data=True,
      scripts=['doorsale/bin/doorsale-admin.py'],
      install_requires=['Django>=1.6,<1.7',
                        'django-pipeline',
                        'Pillow',
                        'paypalrestsdk',
                        'stripe'],
)