#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Oct 22, 2015 '
__author__= 'samuel'

import pytest
from pyramid import testing
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.pool import NullPool
import transaction

from scarab.test.common.utils import db_config
import tempfile
import os
from scarab.scripts.initializedb import initialization

from scarab.models import Base
from scarab.models import DBSession

@pytest.fixture(scope='module')
def engine(request):
    backend_db = db_config('backend_db')
    if backend_db == 'sqlite':
        db_path = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False).name #use tempfile directly
        DB_URL = 'sqlite:///' + db_path
    else:
        DB_URL = db_config('sqlalchemy.url')
    print 'using DB: %s' % DB_URL
    eng = create_engine(DB_URL, poolclass=NullPool)

    DBSession.configure(bind=eng)
    Base.metadata.bind = DBSession.get_bind()
    with transaction.manager as tm:
        Base.metadata.create_all(DBSession.get_bind())
    print '(db.py)using DBSession: %s' % DBSession.get_bind()
    print '(db.py)engine: %s' % eng
    #initialization(Base=Base, DBSession=DBSession, engine=eng, drop_all=False)

    def fin():
        if DBSession.dirty:
            transaction.commit()
            print 'commit transaction'
        DBSession.close()
        print '(DBSession fixture)=>db conntion closed'
        with transaction.manager as tm:
            Base.metadata.drop_all(DBSession.get_bind())
        if backend_db == 'sqlite':
            os.unlink(db_path)
            print 'delete sqlitedb: %s' % db_path
    request.addfinalizer(fin)
    return eng

