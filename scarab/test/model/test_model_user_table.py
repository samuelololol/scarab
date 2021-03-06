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
from scarab.models import DBSession

from utils import id_generator
from test_model_group_table import A_group


@pytest.fixture(scope='module')
def A_user(request, engine_fixture, A_group):
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

    print '(A_user fixture)=> created'
    def fin():
        model = DBSession.query(user_table).filter(user_table.user_id == user.user_id).scalar()
        if model:
            DBSession.delete(model)
            DBSession.flush()
            transaction.commit()
            print '(A_user fixture)=> delete'
        if DBSession.dirty:
            transaction.commit()
    request.addfinalizer(fin)
    return user


def test_query_user(engine_fixture, A_user):
    user_table = models.account.User_TB
    model = DBSession.query(user_table).filter(user_table.user_name == A_user.user_name).scalar()
    assert model.user_name == A_user.user_name

def test_modify_user(engine_fixture, A_user):
    user_table = models.account.User_TB

    original_user_id = A_user.user_id
    new_user_name = id_generator(size=5).decode('utf-8')

    with transaction.manager as tm:
        A_user.user_name = new_user_name
        DBSession.flush()
        find_user = DBSession.query(user_table).filter(user_table.user_name == new_user_name).scalar()
        assert A_user.user_id == find_user.user_id

def test_delete_user(engine_fixture, A_group):
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

def test_change_password(engine_fixture, A_user):
    user_table = models.account.User_TB
    original_user_name = A_user.user_name

    with transaction.manager as tm:
        new_user_password = id_generator(size=8)
        A_user.change_password(new_user_password)
        found_user = DBSession.query(user_table).filter(user_table.user_name == original_user_name).scalar()
        success, msg = found_user.pwd_validate(original_user_name, new_user_password)
        print msg
        assert success == True

def test_user_to_json(engine_fixture, A_user, MockedRequest):
    user_table = models.account.User_TB
    original_user_name = A_user.user_name
    original_user_id = A_user.user_id

    user = DBSession.query(user_table).filter(user_table.user_id == A_user.user_id).scalar()
    user_json = user.to_json(MockedRequest)

    assert True == isinstance(user_json, dict)
    assert user_json['user_id'] == original_user_id
    assert user_json['user_name'] == original_user_name

def test_user_list_to_array(engine_fixture, A_user, MockedRequest):
    user_table = models.account.User_TB
    user_list = user_table.all_to_json_array(MockedRequest)

    assert True == isinstance(user_list, list)
    assert A_user.user_id in [u['user_id'] for u in user_list]
    assert A_user.user_name in [u['user_name'] for u in user_list]

