#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 21, 2015 '
__author__= 'samuel'

import pytest
from scarab.apis.session import SessionAPI
from scarab.test.common.functional import Request, Resource, ScarabApp

import webtest
import json

def test_session_post(ScarabApp):
    res = ScarabApp.post('/api/v1/session', expect_errors=True)
    assert res.status_int == 422

    form = dict()
    form['username'] = 'public'
    form['password'] = '12345678'
    res = ScarabApp.post('/api/v1/session', form)
    print res.body
    assert json.loads(res.body)['success']== True

def test_session_delete(ScarabApp):
    form = dict()
    form['username'] = 'public'
    form['password'] = '12345678'
    res = ScarabApp.post('/api/v1/session', form)
    assert json.loads(res.body)['success']== True

    res = ScarabApp.delete('/api/v1/session')
    assert res.status_int == 204

    res = ScarabApp.delete('/api/v1/session', expect_errors=True)
    assert res.status_int == 403 

def test_session_put(ScarabApp):
    res = ScarabApp.put('/api/v1/session', expect_errors=True)
    assert res.status_int == 404

def test_session_get(ScarabApp):
    res = ScarabApp.get('/api/v1/session', expect_errors=True)
    assert res.status_int == 404

