#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Oct 22, 2015 '
__author__= 'samuel'

import pytest
from pyramid import testing
from sqlalchemy import create_engine
import transaction

from scarab.models import Base
from scarab.models import DBSession as Session

from scarab.test.common.utils import db_config


@pytest.fixture(scope='module')
def DBSession(request):
    DB_URL = db_config('sqlalchemy.url')
    engine = create_engine(DB_URL)
    connection = engine.connect()
    print '(DBSession fixture)=> db connection established'
    Session.configure(bind=engine)

    def fin():
        if Session.dirty:
            transaction.commit()
            print 'commit transaction'
        Session.close()
        connection.close()
        print '(DBSession fixture)=>db conntion closed'
    request.addfinalizer(fin)
    return Session()

