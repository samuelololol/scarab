#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Mar 06, 2014 '
__author__= 'samuel'
import logging
logger = logging.getLogger(__name__)
 
from pyramid.security import remember
from scarab.models.account import User_TB
from scarab.models import DBSession

def login(request, username, password):
    if username == None or username == '':
        err_msg = 'empty username'
        logger.warning(err_msg)
        return False, err_msg

    logger.debug('username: %s password: %s' % (username, password))
    logger.debug('what is my DBSession engine: %s' % DBSession.get_bind())
    user = DBSession.query(User_TB).filter(User_TB.user_name == username.decode('utf-8')).scalar()

    headers = None
    success  = False
    if user:
        success = True
        success, message = user.pwd_validate(username, password)
        if success:
            headers = remember(request, username)
    else:
        logger.warning('user: %s does not exist' % username)

    return success, headers

