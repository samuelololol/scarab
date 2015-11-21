#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.response import Response
from pyramid.view import view_config

from scarab.utils.utils import get_nationalgeographic_image_url


@view_config(route_name='scarab.page_login',
             renderer='scarab:templates/login.jinja2',
             request_method='GET')
def login(request):
    #/login
    image_url= get_nationalgeographic_image_url()
    return {'image_url': image_url}

