Doorsale
========
[![Build Status](https://travis-ci.org/mysteryjeans/doorsale.svg?branch=master)](https://travis-ci.org/mysteryjeans/doorsale)

Doorsale is open source e-commerce solution, simplicity are features designed to thrive sales, which are reaching to be production ready.

To see Doorsale in action, visit [Demo](http://doorsale-demo.fanaticlab.com) site.


## Setting up Doorsale e-commerce

[Doorsale demo](https://github.com/mysteryjeans/doorsale-demo) repository is for quickly getting up and running e-commerce site on your local workstation, its readme contains all steps to setting up a site.

Demo repository is following master branch on Doorsale, so you should pull changes frequently to keep things synchronized and running smoothly, see [demo project](https://github.com/mysteryjeans/doorsale-demo) readme for more details.


## Development

Doorsale is **not** production ready, there are few tasks left in completeness, listed as follows.

- Backoffice administration
- Unit tests
- New project creation script (doorsale-admin.py)
- Initialize database command for populating lookup tables (Convert initial.sql script to django command "createdb")


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
