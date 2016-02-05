[![Build Status](https://travis-ci.org/samuelololol/scarab.svg?branch=v0.2-branch)](https://travis-ci.org/samuelololol/scarab)
![logo][2]
# scarab

A custom API server based on Python Pyramid framework

## Getting Started

### Prepare the database

You could create your postgres via docker(optional, or you could simply use sqlite instead) 

    $ docker run -d -e POSTGRES_DB=postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres 

or just edit the sqlalchemy setting in `development.ini`.


### Install and run in virtualenv

    (venv)$ cd <directory containing this file>
    (venv)$ venv/bin/python setup.py develop
    (venv)$ venv/bin/initialize_scarab_db development.ini
    (venv)$ venv/bin/pserve development.ini

## TODO

* make it to a [scaffold](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/scaffolding.html).


[2]: https://raw.github.com/samuelololol/scarab/master/.logo/2.jpg

