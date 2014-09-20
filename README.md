Doorsale
========
[![Build Status](https://travis-ci.org/mysteryjeans/doorsale.svg?branch=master)](https://travis-ci.org/mysteryjeans/doorsale)

Doorsale is open source e-commerce solution, simplicity are features designed to thrive sales, which are reaching to be production ready.

To see Doorsale in action, visit [Demo](http://doorsale-demo.fanaticlab.com) site.


## Setting up Doorsale e-commerce

[Doorsale demo](https://github.com/mysteryjeans/doorsale-demo) repository is for quickly getting up and running e-commerce site on your local workstation, its readme contains all steps to setting up a site.

When you have enough testing on prepopulated data in demo projects, starting your own site from skretch is similar to creating project in Django.

Create a virtualenv for your own e-commerce project

```
$ virtualenv doorsale_env && source doorsale_env/bin/activate
```

Install the latest development version

```
$ pip install --upgrade git+https://github.com/mysteryjeans/doorsale.git#egg=Doorsale
```

Create a e-commerce project using doorsale-admin.py

```
$ doorsale-admin.py startproject doorsale_site
```

Create a database, new django project use SQLite by default, if you are new to databases this is good choice to start

```
$ python manage.py syncdb
```

Assuming [node.js](http://nodejs.org/) already installed, let's verify that your site works, run development server and visit [http://127.0.0.1:8000](http://127.0.0.1:8000), you will see products catalog page with no products and categories

```
$ python manage.py runserver
```

Django-Pipeline settings is configured to use [Less](http://lesscss.org/#using-less-installation) & [Yuglify](https://github.com/yui/yuglify) node.js packages for static files compression. When you deploy your site with collectstatic command these packages will be called. You can install both packages with [npm](https://www.npmjs.org/) (node.js package manager).

```
$ npm install -g less yuglify 
```

Demo repository is following master branch on Doorsale, so you should pull changes frequently to keep things synchronized and running smoothly, see [demo project](https://github.com/mysteryjeans/doorsale-demo) readme for more details.


## Development

Doorsale is yet to be production ready, there are few tasks left in completeness, listed as follows.

- Unit tests
- Backoffice administration


## Built With

- [Django](https://github.com/django/django) &mdash; Web development framework for python, we utilizes full stack.
- [LESS](https://github.com/less/less.js) &mdash; Our styling totally done in LESS, a preprocessor for CSS.
- [Django-Pipeline](https://github.com/cyberdelia/django-pipeline) &mdash; We use django-pipeline to compile & compress LESS and also Javascript before deployment.
- [PostgreSQL](http://www.postgresql.org/) &mdash; Our primary database is PostgreSQL, although project intended to support all databases that Django supports.


## Contributing

Doorsale is free and open-source, we support and encourages an active heathly community that accepts contributions from the public – including you!

We look forward to seeing your pull requests!


## Screenshot

![Doorsale Demo Screenshot](https://raw.github.com/mysteryjeans/doorsale-demo/master/media/images/demo-screenshot.png)
