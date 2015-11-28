#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 28, 2015 '
__author__= 'samuel'
import logging
FORMAT = "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logging.getLogger().addHandler(logging.StreamHandler())

import sys
import ConfigParser
import io

import pytest
import tempfile
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy.pool import NullPool
from scarab.models import DBSession, Base
from scarab.scripts.initializedb import initialization

import os
import webtest
from webtest import TestApp
from scarab import main

def db_config(key):
    config_path = os.path.dirname(__file__)    # scarab/scarab/test
    config_path = os.path.dirname(config_path) # scarab/scarab
    config_path = os.path.dirname(config_path) # scarab
    config_path = os.path.join(config_path, 'development.ini') #scarab/development.ini
    with open(config_path, 'r') as f:
        config_content = f.read()
    if sys.version_info[0:2] == (2,6):
        config = ConfigParser.RawConfigParser()
    else:
        config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(config_content))
    DB_URL = config.get('app:main', key)
    return DB_URL

@pytest.fixture(scope='session')
def sqlite_engine_fixture(request):
    db_path = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False).name #use tempfile directly
    DB_URL = 'sqlite:///' + db_path
    engine = create_engine(DB_URL, poolclass=NullPool)
    connection = engine.connect()
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    print '(sqlite_engine_fixture) created, sqlite file: %s' % db_path
    def fin():
        DBSession.close()
        DBSession.remove()
        connection.close()
        os.unlink(db_path)
        print '(sqlite_engine_fixture) delete, remove sqlitedb file: %s' % db_path
    request.addfinalizer(fin)
    return engine

@pytest.fixture(scope='module')
def ScarabApp(request):
    settings = {'sqlalchemy.url':     db_config('sqlalchemy.url'),
                'backend_db':         db_config('backend_db'),
                'pyramid.includes':   ['pyramid_tm', 'pyramid_jinja2'],
                'jinja2.directories': 'scarab:templates',
                'scarab.auth_secret': '123abc',
                }
    initialization(engine=DBSession.get_bind(), drop_all=True)
    DBSession.close()
    app = main({}, **settings)
    testapp = TestApp(app)
    return testapp

