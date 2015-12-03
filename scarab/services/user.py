#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scarab.models import DBSession
from scarab.models.account import User_TB

def get_all_users_info(request):
    success = True
    success, data = User_TB.all_to_json_array(request)
    return success, data

def get_user_info(request, user_id):
    success = True
    u = DBSession.query(User_TB).filter(User_TB.user_id == user_id).scalar()
    success, data = u.to_json(request)
    return success, data

