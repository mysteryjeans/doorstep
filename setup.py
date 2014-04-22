import os
import sys

from setuptools import setup, find_packages



# Dynamically calculate the version based on django.VERSION.
version = __import__(   'doorsale').get_version()



setup(name='Doorsale',
      version=version,
      url='http://github.com/mysteryjeans/doorsale',
      author='Faraz Masood Khan',
      author_email='faraz@fanaticlab.com',
      description='The powerful e-commerce solution for Django.',
      license='GPLv2',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['Django',
                        'django-pipeline',
                        'Pillow'],
      )