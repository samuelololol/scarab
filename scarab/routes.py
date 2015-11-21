#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Feb 13, 2014 '
__author__= 'samuel'

api_prefix = '/api/v'
api_version = 1

def api_routes(config):
    #apis
    config.add_route('api_session',  api_prefix + str(api_version) + '/session')

    #pages
    config.add_route('scarab.page_login', '/login')
    config.add_route('scarab.page_home', '/')

    #static at bottom
    config.add_static_view('static', 'static', cache_max_age=3600)

