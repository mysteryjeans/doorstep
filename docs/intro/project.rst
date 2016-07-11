.. _ref-project:

=======
Project
=======

I'll assume you have :doc:`Doorsale installed <install>` already. You can
tell which version by running the following command:

.. code-block:: console

    $ python -c "import doorsale; print(doorsale.get_version())"

If Doorsale is installed, you should see the version of your installation. If it
isn't, you'll get an error telling "No module named doorsale".

Start new project
=================

If you haven't develop with Django_ before, this documentation doesn't cover you
for Django development. Doorsale itself follows Django philosophy and uses,
extends or even copies it where ever possible.

Start your own e-commerce project using ``doorsale-admin.py``, it simple wrapper
around Django's own ``django-admin.py``:

.. code-block:: console

    $ doorsale-admin.py startproject ecomstore

Now that your own site is created, lets change directory to ecomstore & create
database tables by running following command. This will create all tables
required by Django & Doorsale. Default database is SQLite_ which is a good
starting point, you can later switch to your favorite databases_ that are
supported by Django.

.. code-block:: console

    $ python manage.py migrate

.. _Django: https://www.djangoproject.com
.. _SQLite: https://www.sqlite.org
.. _databases: https://docs.djangoproject.com/en/stable/ref/databases/

Run your site
=============

Let's run the builtin Django development server and verify by visiting
http://127.0.0.1:8000, if all works well you will see web page with not products
& listings. If you see error compiling CSS or Javascript than head over to
:doc:`installation <install>` and install LESS & Yuglify nodejs packages.

.. code-block:: console

    $ python manage.py runserver

Create site admin
=================

Let's create site admin or in Django term superuser. There are two ways to
create site admin, by Django's builtin command or the first user
that register to the site will automatically becomes site admin.

.. code-block:: console

    $ python manage.py createsuperuser
