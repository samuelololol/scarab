#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 27, 2015 '
__author__= 'samuel'

import pytest
import webtest

def test_session_get(engine_fixture, ScarabApp):
    print 'test_session_get()'
    res = ScarabApp.get('/')
    assert 'Welcome to' in res.body

