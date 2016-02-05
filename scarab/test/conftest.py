#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 28, 2015 '
__author__= 'samuel'
import logging
FORMAT = "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)

import sys
import ConfigParser
import io
import json
import os

import pytest
import tempfile
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy.pool import NullPool
from scarab.models import DBSession, Base
from scarab.scripts.initializedb import initialization

import webtest
from pyramid.paster import get_app
from pyramid.paster import get_appsettings
from webtest import TestApp
from scarab import main

from pyramid.testing import DummyRequest

config_path = os.path.dirname(__file__)    # scarab/scarab/test
config_path = os.path.dirname(config_path) # scarab/scarab
config_path = os.path.dirname(config_path) # scarab
config_path = os.path.join(config_path, 'development.ini') #scarab/development.ini

def get_config_settings(key):
    global config_path
    return get_appsettings(config_path)[key]

@pytest.fixture(scope='session')
def engine_fixture(request):
    backend_db = 'sqlite' if 'sqlite://' in get_config_settings('sqlalchemy.url') else 'postgres'
    logger.debug('backend_db: %s' % backend_db)
    if backend_db == 'sqlite':
        db_path = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False).name #use tempfile directly
        DB_URL = 'sqlite:///' + db_path
        engine = create_engine(DB_URL, poolclass=NullPool)
        connection = engine.connect()
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine
        logger.debug('(sqlite_engine_fixture) created, sqlite file: %s' % db_path)
    else:
        DB_URL = get_config_settings('sqlalchemy.url')
        engine = create_engine(DB_URL)
        connection = engine.connect()
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine
        logger.debug('(postgres_engine_fixture) created, postgres url: %s' % DB_URL)
    def fin():
        DBSession.close()
        DBSession.remove()
        connection.close()
        if backend_db == 'sqlite':
            os.unlink(db_path)
            logger.debug('(sqlite_engine_fixture) delete, remove sqlitedb file: %s' % db_path)
        else:
            logger.debug('(postgres_engine_fixture) fin with postgresdb url: %s' % DB_URL)
    request.addfinalizer(fin)
    #return engine
    return backend_db

@pytest.fixture(scope='session')
def ScarabApp(request):
    global config_path
    app = get_app(config_path)
    testapp = TestApp(app)
    return testapp

@pytest.fixture(scope='function')
def MockedRequest(request):
    backend_db = 'sqlite' if 'sqlite://' in get_config_settings('sqlalchemy.url') else 'postgres'
    scarab_settings = {'backend_db': backend_db}
    req = DummyRequest()
    req.scarab_settings = scarab_settings
    return req


#for functional API tests
@pytest.fixture(scope='function')
def LoggedInApp(ScarabApp):
    form = {'username': 'public', 'password': '12345678'}
    res = ScarabApp.post('/api/v1/session', form)
    assert json.loads(res.body)['success'] == True
    return ScarabApp

