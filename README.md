Doorstep
========
[![Build Status](https://travis-ci.org/mysteryjeans/doorstep.svg?branch=master)](https://travis-ci.org/mysteryjeans/doorstep)

Doorstep is open source e-commerce solution, simplicity in designed is to thrive sales and reduce development effort. Please read the documentation http://doorstep.readthedocs.io

## Setting up Doorstep e-commerce

[Doorstep demo](https://github.com/mysteryjeans/doorstep-demo) repository is for quickly getting up and running e-commerce site on your local workstation, its readme contains all steps to setting up a site.

When you have enough testing on prepopulated data in demo projects, starting your own site from scratch is similar to creating project in Django.

Create a new virtualenv for your own e-commerce project

```
$ virtualenv doorstep_env && source doorstep_env/bin/activate
```

Install the latest development version from this git repository.

```
$ pip install --upgrade git+https://github.com/mysteryjeans/doorstep.git#egg=Doorstep
```

Create a e-commerce project using doorstep-admin.py instead of using django-admin.py.

```
$ doorstep-admin.py startproject doorstep_site
```

Create database schema by running migrate command, by default django project use SQLite, which off course you can changed in settings.py, if you are new to databases this is good choice to start with. Migrate command will also load initial data in database as well.

```
$ python manage.py migrate
```

Node.js is required for LESS & javascript preprocessing, assuming [node.js](http://nodejs.org/) is already installed, let's verify that your site works, run development server and visit [http://127.0.0.1:8000](http://127.0.0.1:8000), you will see products catalog index page with no products and categories

```
$ python manage.py runserver
```

Django-Pipeline settings is configured to use [LESS](http://lesscss.org/#using-less-installation) & [Yuglify](https://github.com/yui/yuglify) node.js packages for static files preprocessing & compression. When you deploy your site with collectstatic command these packages will be called. You can install both packages with [npm](https://www.npmjs.org/) (node.js package manager).

```
$ npm install -g less yuglify
```

Demo repository is following master branch on Doorstep, so you should pull changes frequently to keep things synchronized and running smoothly, see [demo project](https://github.com/mysteryjeans/doorstep-demo) readme for more details.


## Development

Doorstep is yet to be production ready, there are few features left in completeness are:

- Administration\Backoffice
- Unit tests

## Built With

- [Django](https://github.com/django/django) &mdash; Web development framework for python, we utilizes full stack.
- [LESS](https://github.com/less/less.js) &mdash; Our styling totally done in LESS, a preprocessor for CSS.
- [Django-Pipeline](https://github.com/cyberdelia/django-pipeline) &mdash; We use django-pipeline to compile & compress LESS and also Javascript before deployment.
- [PostgreSQL](http://www.postgresql.org/) &mdash; Our primary database is PostgreSQL, although project intended to support all databases that Django supports.


## Contributing

Doorstep is free and open-source, I support and encourage an active healthy community that accepts contributions from the public – **including you!**

We look forward to seeing your pull requests!


## Screenshot

![Doorstep Demo Screenshot](https://raw.github.com/mysteryjeans/doorstep-demo/bootstrap/media/images/demo-screenshot.png)
![Doorstep Demo Screenshot](https://raw.github.com/mysteryjeans/doorstep-demo/bootstrap/media/images/demo-screenshot.png)
