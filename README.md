Doorstep
========
[![Build Status](https://travis-ci.org/mysteryjeans/doorstep.svg?branch=master)](https://travis-ci.org/mysteryjeans/doorstep)

Doorstep is open source e-commerce solution, simplicity in designed is to thrive sales and reduce development effort. Please read the documentation http://doorstep.readthedocs.io

## Setting up Doorstep e-commerce as Django project

[Doorstep demo](https://github.com/mysteryjeans/doorstep-demo) repository is for quickly getting up and running e-commerce site on your local workstation, its readme contains all steps to setting up a site.

When you have enough testing on prepopulated data in demo projects, starting your own site from scratch is similar to creating project in Django.

Create a new virtualenv for your own e-commerce project

```
$ virtualenv doorstep_env && source doorstep_env/bin/activate
```

Get copy of latest version of Doorstep from Github.

```
$ git clone https://github.com/mysteryjeans/doorstep.git && cd doorstep
```

Install Django and other packages dependencies using requirements.txt in your virtualenv. Doorstep also requires Node.js packages, see details below.

```
$ pip install -r requirements.txt
```

Create database schema by running migrate command, by default Django project use SQLite, if you are new to databases this is good choice to start with. Migrate command will also load initial data in database as well.

```
$ python manage.py migrate
```


## Setting up Doorstep e-commerce as Django App and separate project site

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

Alternatively you can clone repository and export root directory path to python virtualenv site-packages

```
$ git clone https://github.com/mysteryjeans/doorstep.git && cd doorstep
$ echo $(pwd) > ../doorstep_env/lib/python2.7/site-packages/doorstep.pth
```

Create a e-commerce project using doorstep-admin.py instead of using django-admin.py if you have install it using pip.

```
$ doorstep-admin.py startproject doorstep_site
```

If you have exported repository clone path then install Django & other packages dependencies using requirements.txt in your virtualenv first and then create new project site. Doorstep also requires Node.js packages, see details below.

```
$ pip install -r requirements.txt && cd ../
$ doorstep/doorstep/bin/doorstep-admin.py startproject doorstep_site && cd doorstep_site
```

Create database schema by running migrate command, by default django project use SQLite, which off course you can changed in settings.py, if you are new to databases this is good choice to start with. Migrate command will also load initial data in database as well.

```
$ python manage.py migrate
```

## Node.js packages dependency and installation

Django-Pipeline settings is configured to use [LESS](http://lesscss.org/#using-less-installation) & [Yuglify](https://github.com/yui/yuglify) node.js packages for static files preprocessing & compression. When you deploy your site with collectstatic command these packages will be called. You can install both packages with [npm](https://www.npmjs.org/) (node.js package manager).

```
$ npm install -g less yuglify
```

## Running development server for your e-commerce project

Assuming you have installed [node.js](http://nodejs.org/) & packages, let's verify that your site works, run development server and visit [http://127.0.0.1:8000](http://127.0.0.1:8000), you will see products catalog index pages with no products and categories

```
$ python manage.py runserver
```


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

![Doorstep Demo Screenshot](https://raw.github.com/mysteryjeans/doorstep-demo/master/media/images/demo-screenshot.jpg)

![Doorstep Demo Screenshot](https://raw.github.com/mysteryjeans/doorstep-demo/master/media/images/mobile-screenshot.png)

