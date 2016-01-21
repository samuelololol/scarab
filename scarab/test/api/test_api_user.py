#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

import webtest
import json

api_prefix = '/api/v'
api_version = 1

@pytest.mark.api_users
def test_users_get(engine_fixture, LoggedInApp):
    ScarabApp = LoggedInApp

    res = ScarabApp.get(api_prefix + '1' + '/users')
    print "this is data:", json.loads(res.body)['data']
    print engine_fixture
    if engine_fixture == 'sqlite':
        return
    assert json.loads(res.body)['data'][0]['user_id'] == 1
    #assert len(json.loads(res.body)['data']) >= 0

@pytest.mark.api_user
def test_user_get(engine_fixture, LoggedInApp):
    ScarabApp = LoggedInApp

    res = ScarabApp.get(api_prefix + '1' + '/user/1')
    print "this is data:", json.loads(res.body)['data']
    print engine_fixture
    if engine_fixture == 'sqlite':
        return
    assert json.loads(res.body)['data']['user_id'] == 1

