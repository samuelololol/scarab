[![Build Status](https://travis-ci.org/samuelololol/scarab.svg?branch=master)](https://travis-ci.org/samuelololol/scarab)
![logo][2]
# scarab README

## Getting Started

### Prepare the database

You could create your postgres via docker 

    (optional)$ docker run -d -e POSTGRES\_DB=postgres -e POSTGRES\_USER=postgres -e POSTGRES\_PASSWORD=postgres -p 5432:5432 postgres 

or just edit the sqlalchemy setting in `development.ini`.


### Install and run

    (venv)$ cd <directory containing this file>
    (venv)$ venv/bin/python setup.py develop
    (venv)$ venv/bin/initialize_scarab_db development.ini
    (venv)$ venv/bin/pserve development.ini

## ToDo

### Backend

1. add Single Sign-On feature for Facebook, twitter, Google
   * create `Token_TB`
   * create `endpoint_api`
   * create `callback_api`

### FrontEnd

1. home page
    * remove pyramid home page
    * merge `Twitter-BootStrap` to tempalte




[2]: https://raw.github.com/samuelololol/scarab/master/.logo/2.jpg

