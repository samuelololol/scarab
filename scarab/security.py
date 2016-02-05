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

def get_user(request):
    #user_name = unauthenticated_userid(request)
    user_name = request.unauthenticated_userid
    logger.debug('unauthenticated_userid(as username): %s' % user_name)
    if user_name is not None:
        with transaction.manager as tm:
            user_obj = DBSession.query(User_TB).filter(User_TB.user_name == user_name).scalar()
        return user_obj
    logger.debug('get no user')
    return None


def groupfinder(userid, request):
    logger.debug('groupfinder: userid: %s' % userid)
    user = request.user
    return_groups = []
    if user is not None:
        return_groups.append(user.group.group_name.encode('utf-8'))
    logger.debug('groupfinder: groups %s' % return_groups)
    return return_groups

