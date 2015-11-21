#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 21, 2015 '
__author__= 'samuel'
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

from pyramid.security import forget

from formencode import Schema
from formencode import validators
from formencode import Invalid

from scarab.services import session
import json

class Schema_login_post(Schema):
    username = validators.Regex(r'^[a-z][a-zA-Z0-9_.-]{2,19}$', strip=True, not_empty=True)
    password = validators.Regex(r'^[A-Za-z0-9@#$%^&+=]{6,20}$', not_empty=True)
   

@view_defaults(renderer='json')
class SessionAPI(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name='api_session', request_method='POST', permission='view')
    def api_login(self):
        #JSON_BODY = self.request.json_body
        #but arguments are from form not body
        try:
            login_form = {'username': self.request.POST.get('username', None),
                          'password': self.request.POST.get('password', None)}
            params = Schema_login_post.to_python(login_form)
            print params
        except Invalid, invalid_exception:
            err_msg = invalid_exception.unpack_errors()
            logger.warning(err_msg)
            #return HTTPUnprocessableEntity(detail=err_msg)
            rtn = json.dumps({'success': False, 'message': err_msg})
            return HTTPUnprocessableEntity(body=rtn, content_type='application/json') 
        except Exception, e:
            err_msg = str(e)
            logger.error(err_msg, exc_info=1)
            rtn = json.dumps({'success': False, 'message': None})
            return HTTPInternalServerError(body=rtn, content_type='application/json')

        success, headers = session.login(self.request, params['username'], params['password'])
        message = ''
        if success:
            message = 'login success'
            logger.info('user: \'%s\' logged in' % params['username'])
        else:
            message = 'username or password incorrect'
        rtn = json.dumps({'success': success, 'message': message})
        return HTTPCreated(body=rtn, content_type='application/json', headers=headers)


    @view_config(route_name='api_session', request_method='DELETE', permission='login')
    def api_logout(self):
        user_name = self.request.user.user_name
        headers = forget(self.request)
        logger.info('user: \'%s\' logged out' % user_name)
        return HTTPNoContent(headers=headers, content_type='application/json')

