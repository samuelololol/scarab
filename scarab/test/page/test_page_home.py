#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 27, 2015 '
__author__= 'samuel'

import pytest
from scarab.test.common.functional import ScarabApp

import webtest

def test_session_get(ScarabApp):
    print 'test_session_get()'
    res = ScarabApp.get('/')
    assert 'Welcome to' in res.body

