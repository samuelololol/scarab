#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pytest
import transaction
from pyramid import testing
import time
import os
import hashlib

from scarab import models

#import os,sys,inspect
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0,parentdir) 
#from common.db import DBSession
#from common.utils import id_generator
from scarab.test.common.db import DBSession
from scarab.test.common.utils import id_generator
from test_group_table import A_group


@pytest.fixture(scope='module')
def A_user(request, DBSession, A_group):
    user_table = models.account.User_TB

    user_name=id_generator(size=25).decode('utf-8')
    salt = os.urandom(26).encode('hex')
    password = os.urandom(10).encode('hex')

    with transaction.manager as tm:
        success, user = user_table.create(
                            user_name = user_name,
                            password=password,
                            activated=True,
                            group_id=A_group.group_id
                            )
        assert success == True

    print '(fixture)=>A_user created'
    def fin():
        model = DBSession.query(user_table).filter(user_table.user_id == user.user_id).scalar()
        if model:
            DBSession.delete(model)
            DBSession.flush()
            transaction.commit()
            print '(fixture)=>A_user delete'
        if DBSession.dirty:
            transaction.commit()
    request.addfinalizer(fin)
    return user


def test_query_user(DBSession, A_user):
    user_table = models.account.User_TB
    model = DBSession.query(user_table).filter(user_table.user_name == A_user.user_name).scalar()
    assert model.user_name == A_user.user_name

def test_modify_user(DBSession, A_user):
    user_table = models.account.User_TB

    original_user_id = A_user.user_id
    new_user_name = id_generator(size=5).decode('utf-8')

    with transaction.manager as tm:
        A_user.user_name = new_user_name
        DBSession.flush()
        find_user = DBSession.query(user_table).filter(user_table.user_name == new_user_name).scalar()
        assert A_user.user_id == find_user.user_id

def test_delete_user(DBSession, A_group):
    user_table = models.account.User_TB

    user_name=id_generator(size=25).decode('utf-8')
    salt = os.urandom(26).encode('hex')
    password = os.urandom(10).encode('hex')

    with transaction.manager as tm:
        success, user = user_table.create(
                            user_name = user_name,
                            password=password,
                            activated=True,
                            group_id=A_group.group_id
                            )
        assert success == True
        #delete
        DBSession.delete(user)
        DBSession.flush()
        model = DBSession.query(user_table).filter(user_table.user_id == user.user_id).first()
        assert model == None

def test_change_password(DBSession, A_user):
    user_table = models.account.User_TB
    original_user_name = A_user.user_name

    with transaction.manager as tm:
        new_user_password = id_generator(size=8)
        A_user.change_password(new_user_password)
        found_user = DBSession.query(user_table).filter(user_table.user_name == original_user_name).scalar()
        success, msg = found_user.pwd_validate(original_user_name, new_user_password)
        print msg
        assert success == True

