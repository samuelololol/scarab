#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 21, 2015 '
__author__= 'samuel'

import pytest
from scarab.test.common.utils import id_generator
from webtest import TestApp
from pyramid import testing


from scarab import main
from scarab.models import DBSession, Base
from sqlalchemy.pool import NullPool
from sqlalchemy import engine_from_config, create_engine
from scarab.scripts.initializedb import initialization
import transaction
from scarab.models.account import User_TB

from scarab.test.common.utils import db_config
import tempfile
import os

@pytest.fixture(scope='function')
def Request(request):
    return testing.DummyRequest()

@pytest.fixture(scope='function')
def Resource(request):
    return testing.DummyResource()

@pytest.fixture(scope='module')
def ScarabApp(request):
    settings = {'sqlalchemy.url': db_config('sqlalchemy.url'),
                'backend_db': db_config('backend_db'),
                'pyramid.includes': ['pyramid_tm', 'pyramid_jinja2'],
                'jinja2.directories': 'scarab:templates',
                'scarab.auth_secret': '123abc',
                }
    backend_db = db_config('backend_db')
    if backend_db == 'sqlite':
        db_path = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False).name #use tempfile directly
        DB_URL = 'sqlite:///' + db_path
        settings['sqlalchemy.url'] = DB_URL
    else:
        DB_URL = db_config('sqlalchemy.url')
    print 'using DB: %s' % DB_URL
    engine = create_engine(DB_URL, poolclass=NullPool)
    connection = engine.connect()
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    #initial
    initialization(engine=engine, drop_all=True)
    DBSession.close()
    app = main({}, **settings)
    def fin():
        if DBSession.dirty:
            transaction.commit()
            print 'commit transaction'
        DBSession.remove()
        DBSession.close()
        connection.close()
        if backend_db == 'sqlite':
            os.unlink(db_path)
            print 'delete sqlitedb: %s' % db_path
    DBSession.remove()
    request.addfinalizer(fin)
    testapp = TestApp(app)
    return testapp
    
