#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 21, 2015 '
__author__= 'samuel'

import logging
logger = logging.getLogger(__name__)

from scarab.models import DBSession
from scarab.models import Base
from scarab.common import ModelMethod

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from sqlalchemy.types import (
        BigInteger,
        Integer,
        String,
        Boolean,
        DateTime,
        Unicode,
        UnicodeText,
        Float,
        )

import datetime
import os
import hashlib


class Group_TB(Base):
    __tablename__ = 'groupt'

    group_id        = Column(Integer,      nullable=False, unique=True, primary_key=True, autoincrement=True)
    group_name      = Column(Unicode(255), nullable=False, unique=True, index=True)
    description     = Column(Unicode(255), nullable=True,  unique=False)
    createddatetime = Column(DateTime,     nullable=False)
    updateddatetime = Column(DateTime,     nullable=False)

    users = relationship('User_TB', backref=backref('group', order_by=group_id))

    def __init__(self, *args, **kwargs):
        self.createddatetime = datetime.datetime.utcnow()
        self.updateddatetime = datetime.datetime.utcnow()
        super(Group_TB, self).__init__(*args, **kwargs)


class User_TB(Base):
    __tablename__ = 'usert'

    user_id         = Column(Integer,      nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_name       = Column(Unicode(255), nullable=False, unique=True, index=True)
    description     = Column(Unicode(255), nullable=True,  unique=False)
    activated       = Column(Boolean,      nullable=False, unique=False)
    password        = Column(String(255),  nullable=False, unique=False)
    salt            = Column(String(255),  nullable=False, unique=False)
    createddatetime = Column(DateTime,     nullable=False)
    updateddatetime = Column(DateTime,     nullable=False)

    #fk
    group_id      = Column(Integer, ForeignKey('groupt.group_id'), nullable=False, unique=False)

    def __init__(self, *args, **kwargs):
        self.createddatetime = datetime.datetime.utcnow()
        self.updateddatetime = datetime.datetime.utcnow()
        super(User_TB, self).__init__(*args, **kwargs)

    @classmethod
    @ModelMethod(logger)
    def create(cls, user_name, password, activated, group_id, description=None):
        global DBSession
        salt = os.urandom(26).encode('hex')
        logger.debug('create salt: %s' % salt)
        hashed_pwd = hashlib.sha512(salt + password).hexdigest()
        model = cls(user_name=user_name, description=description, password=hashed_pwd,
                    salt=salt, activated=activated, group_id=group_id)
        DBSession.add(model)
        DBSession.flush()
        logger.info('user %s created' % user_name)
        rtn = (True, model)
        return rtn

    @ModelMethod(logger)
    def change_password(self, new_password):
        global DBSession
        hashed_pwd = hashlib.sha512(self.salt + new_password).hexdigest()
        self.password = hashed_pwd
        DBSession.add(self)
        DBSession.flush()
        logger.info('user %s password changed' % self.user_name)
        rtn = (True, None)
        return rtn

    @classmethod
    @ModelMethod(logger)
    def all_to_json_array(cls, request):
        success = True
        if request.scarab_settings['backend_db'] == 'sqlite':
            json_array = [{'error': 'sqlite does not implement array_to_json()'}]
        elif request.scarab_settings['backend_db'] == 'postgres':
            logger.debug('execut array_to_json()')
            json_array = cls._pg_all_to_json_array()
        json_array = [] if json_array == None else json_array
        return success, json_array

    @classmethod
    def _pg_all_to_json_array(cls):
        sql_expression = \
            """
            select array_to_json(array_agg(t)) from (
                select 
                    user_id,
                    group_id,
                    description,
                    user_name,
                    activated,
                    createddatetime,
                    updateddatetime
                from %s) t; """ % (cls.__tablename__)
        users = DBSession.execute(sql_expression).scalar()
        logger.debug('json users: %s' % users)
        return users

    @ModelMethod(logger)
    def pwd_validate(self, name, password):
        test_pwd = hashlib.sha512(self.salt + password).hexdigest()

        result = 0
        db_pass_len = len(self.password)
        test_pass_len = len(test_pwd)
        result = db_pass_len ^ test_pass_len
        if result != 0:
            logger.warning('user: %s password length incorrect' % name)
            return (False, 'password incorrect.')

        for i in xrange(db_pass_len):
            result += (ord(test_pwd[i]) ^ ord(self.password[i]))

        if result == 0:
            return (True, 'password is correct')
        else:
            logger.warning('user: %s password incorrect' % name)
            return (False, 'password is incorrect.')

    @ModelMethod(logger)
    def to_json(self, request):
        success = True
        json_obj = {}
        if request.scarab_settings['backend_db'] == 'sqlite':
            json_obj = self._manual_to_json()
        elif request.scarab_settings['backend_db'] == 'postgres':
            logger.debug('execut row_to_json()')
            json_obj = self._pg_row_to_json()

        logger.debug('this is json_obj: %s' % json_obj)
        if json_obj != None:
            json_obj.pop('password')
            json_obj.pop('salt')
        else:
            json_obj = {}
        return success, json_obj

    def _manual_to_json(self):
        logger.warning('sqlite does not implement row_to_json()')
        return None

    def _pg_row_to_json(self):
        sql_expression = \
            """
            select row_to_json(u) from (
                select *
                from %s where user_id = %s) u;
            """ % (self.__tablename__, self.user_id)
        user = DBSession.execute(sql_expression).scalar()
        logger.debug('json user: %s' % user)
        return user

