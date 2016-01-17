#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.view import forbidden_view_config
from pyramid.response import Response
from pyramid.httpexceptions import (
        HTTPFound,
        HTTPCreated,
        HTTPNoContent,
        HTTPUnprocessableEntity,
        HTTPInternalServerError,
        HTTPUnauthorized,
        )

import formencode
from formencode import Schema
from formencode import validators
from formencode import Invalid

from scarab.services.user import get_all_users_info
from scarab.services.user import get_user_info


@view_defaults(renderer='json')
class UserAPI(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name='api_users', request_method='GET', permission='login')
    def api_users_get(self):
        success, data = get_all_users_info(self.request)
        return {'name': 'users', 'method': 'GET', 'data': data}

    @view_config(route_name='api_user', request_method='GET', permission='login')
    def api_user_get(self):
        user_id = self.request.matchdict['id']
        success, data = get_user_info(self.request, user_id)
        return {'name': 'user', 'method': 'GET', 'data': data}

