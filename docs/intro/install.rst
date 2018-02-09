.. _ref-install:

============
Installation
============

Before you can start with your e-commerce project, lets install Doorstep.


Virtual environment
==========================

Create a new `virtual environment`_ for Doorstep, its isolated Python environment
which are more practical than installing Doorstep systemwide. They also allow
installing packages without root privileges, you may create separate virtualenv_
for each of your e-commerce site.

.. code-block:: console

     $ virtualenv doorstep_env && source doorstep_env/bin/activate

.. _virtualenv: http://www.virtualenv.org/
.. _virtual environment: http://www.virtualenv.org/

Install Doorstep
================

Recommend way to install Doorstep is via pip_, it will be easy
to upgrade to latest version. Alternatively you can download repository and
install with via setuptools_ ``python setup.py install``

.. code-block:: console

   $ pip install --upgrade git+https://github.com/mysteryjeans/doorstep.git#egg=Doorstep

.. _pip: https://pip.pypa.io/
.. _setuptools: https://pypi.python.org/pypi/setuptools

Install LESS & Yuglify
======================

Install LESS_ & Yuglify_ nodejs packages, which will be used by
django-pipeline_ for javascript and CSS processing, nodejs_
setup also include npm_ package manager.

.. code-block:: console

   $ npm install -g less yuglify

.. _nodejs: https://nodejs.org
.. _npm: https://www.npmjs.com
.. _LESS: http://lesscss.org
.. _Yuglify: https://github.com/yui/yuglify
.. _django-pipeline: https://github.com/jazzband/django-pipeline
