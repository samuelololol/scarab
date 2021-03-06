#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 21, 2015 '
__author__= 'samuel'

import pytest

import webtest
import json

def test_session_post(engine_fixture, ScarabApp):
    print 'test_session_post()'
    res = ScarabApp.post('/api/v1/session', expect_errors=True)
    print 'fail response status code: %s' % res.status_int
    assert res.status_int == 422

    #must get a form from page!
    res = ScarabApp.get('/login')
    form = res.forms[0]
    form['username'] = 'public'
    form['password'] = '12345678'
    res = form.submit()
    print res.body
    assert json.loads(res.body)['success']== True

def test_session_post_fail(engine_fixture, ScarabApp):
    print 'test_session_post_fail()'
    form = dict()
    form['username'] = 'public'
    form['password'] = '123456'
    res = ScarabApp.post('/api/v1/session', form, expect_errors=True)
    print res.body
    assert json.loads(res.body)['success']== False


def test_session_delete(engine_fixture, LoggedInApp):
    ScarabApp = LoggedInApp

    res = ScarabApp.delete('/api/v1/session')
    assert res.status_int == 204

    res = ScarabApp.delete('/api/v1/session', expect_errors=True)
    assert res.status_int == 403 

def test_session_put(engine_fixture, ScarabApp):
    print 'test_session_put()'
    res = ScarabApp.put('/api/v1/session', expect_errors=True)
    assert res.status_int == 404

def test_session_get(engine_fixture, ScarabApp):
    print 'test_session_get()'
    res = ScarabApp.get('/api/v1/session', expect_errors=True)
    assert res.status_int == 404

