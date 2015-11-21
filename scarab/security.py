#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Mar 06, 2014 '
__author__= 'samuel'

from pyramid.security import unauthenticated_userid

from scarab.models.account import User_TB
from scarab.models import DBSession
import transaction


def get_user(request):
    user_name = unauthenticated_userid(request)
    if user_name is not None:
        with transaction.manager as tm:
            user_obj = DBSession.query(User_TB).filter(User_TB.user_name == user_name).scalar()
        return user_obj
    return None


def groupfinder(userid, request):
    user = request.user
    if user is not None:
        return [ user.group.group_name.encode('utf-8') ]
    else:
        []


def main():
    pass

if __name__ == '__main__':
    main()
