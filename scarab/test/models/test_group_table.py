#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pytest
import transaction
from pyramid import testing
import time

from scarab import models

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from common.db import DBSession
from common.utils import id_generator


@pytest.fixture(scope='module')
def A_group(request, DBSession):
    group_table = models.account.Group_TB
    with transaction.manager as tm:
        group = group_table(group_name=id_generator(size=25).decode('utf-8'))
        DBSession.add(group)
        DBSession.flush()
    print "(fixture)=>A_group created"
    def fin():
        model = DBSession.query(group_table).filter(group_table.group_id == group.group_id).scalar()
        if model:
            DBSession.delete(model)
            DBSession.flush()
            transaction.commit()
            print '(fixture)=>A_group delete'
        if DBSession.dirty:
            transaction.commit()
    request.addfinalizer(fin)
    return group


def test_query_group(DBSession, A_group):
    group_table = models.account.Group_TB
    group = DBSession.query(group_table).filter(group_table.group_name == A_group.group_name).scalar()
    assert group.group_name == A_group.group_name

def test_modify_group(DBSession, A_group):
    group_table = models.account.Group_TB
    model = DBSession.query(group_table).filter(group_table.group_name == A_group.group_name).scalar()
    assert model.group_id == A_group.group_id

    original_group_id = model.group_id
    new_group_name = id_generator(size=5).decode('utf-8')

    with transaction.manager as tm:
        A_group.group_name = new_group_name
        DBSession.flush()
        find_group = DBSession.query(group_table).filter(group_table.group_name == new_group_name).scalar()
        assert find_group.group_id == original_group_id

def test_delete_group(DBSession):
    group_table = models.account.Group_TB
    new_group_name = id_generator(size=25).decode('utf-8')
    with transaction.manager as tm:

        #create
        new_model = group_table(group_name=new_group_name)
        DBSession.add(new_model)
        DBSession.flush()

        model = DBSession.query(group_table).filter(group_table.group_name == new_group_name).scalar()
        assert model

        #delete
        DBSession.delete(model)
        DBSession.flush()

        model = DBSession.query(group_table).filter(group_table.group_name == new_group_name).first()
        assert model == None

