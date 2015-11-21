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
from sqlalchemy import engine_from_config
from scarab.scripts.initializedb import initialization
import transaction


from scarab.test.common.utils import db_config

@pytest.fixture(scope='function')
def Request(request):
    return testing.DummyRequest()

@pytest.fixture(scope='function')
def Resource(request):
    return testing.DummyResource()

@pytest.fixture(scope='session')
def ScarabApp(request):
    settings = {'sqlalchemy.url': db_config('sqlalchemy.url'),
                'backend_db': db_config('backend_db'),
                'pyramid.includes': ['pyramid_tm', 'pyramid_jinja2'],
                'jinja2.directories': 'scarab:templates',
                'scarab.auth_secret': '123abc',
                }

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    #initial
    initialization(Base=Base, DBSession=DBSession, engine=engine, drop_all=True)

    app = main({}, **settings)
    def fin():
        if DBSession.dirty:
            transaction.commit()
            print 'commit transaction'
        #DBSession.close()
    request.addfinalizer(fin)
    testapp = TestApp(app)
    return testapp
    
