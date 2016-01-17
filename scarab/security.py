#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Mar 06, 2014 '
__author__= 'samuel'
import logging
logger = logging.getLogger(__name__)

from pyramid.security import unauthenticated_userid

from scarab.models.account import User_TB
from scarab.models import DBSession
import transaction

#security
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

def get_user(request):
    user_name = unauthenticated_userid(request)
    if user_name is not None:
        with transaction.manager as tm:
            user_obj = DBSession.query(User_TB).filter(User_TB.user_name == user_name).scalar()
        return user_obj
    return None


def groupfinder(userid, request):
    logger.debug('groupfinder: userid: %s' % userid)
    user = request.user
    return_groups = []
    if user is not None:
        return_groups.append(user.group.group_name.encode('utf-8'))
    logger.debug('groupfinder: groups %s' % return_groups)
    return return_groups


def apply_multiauth(config, secret):
    authn_policy = AuthTktAuthenticationPolicy(secret, callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    return config

