#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import inspect
import traceback
from scarab.models import DBSession
from scarab.models.account import User_TB

logger = logging.getLogger(__name__)

def get_all_users_info(request):
    try:
        rtn = (True, User_TB.all_to_json_array(request))
    except Exception, e:
        err_info = (User_TB.__tablename__, inspect.stack()[0][3], traceback.format_exc())
        logger.error('%s:%s, traceback: %s' % err_info, exc_info=True)
        rtn = (False, None)
    return rtn

def get_user_info(request, user_id):
    try:
        u = DBSession.query(User_TB).filter(User_TB.user_id == user_id).scalar()
        if u == None:
            logger.warning('user(user_id: %s) not exist.' % user_id)
            return (False, None)
        rtn = (True, u.to_json(request))
    except Exception, e:
        err_info = ('user_id(%s)' % user_id, inspect.stack()[0][3], traceback.format_exc())
        logger.error('%s:%s, traceback: %s' % err_info, exc_info=True)
        rtn = (False, None)
    return rtn

