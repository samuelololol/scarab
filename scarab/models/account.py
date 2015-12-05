#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from scarab.models import DBSession
from scarab.models import Base

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
        return (True, model)

    def change_password(self, new_password):
        global DBSession
        hashed_pwd = hashlib.sha512(self.salt + new_password).hexdigest()
        self.password = hashed_pwd
        DBSession.add(self)
        DBSession.flush()
        logger.info('user %s password changed' % self.user_name)
        return (True, None)

    @classmethod
    def all_to_json_array(cls, request, ignore=['password', 'salt']):
        if request.scarab_settings['backend_db'] == 'sqlite':
            json_array = cls._manual_all_to_json_array(ignore=ignore)
        elif request.scarab_settings['backend_db'] == 'postgres':
            json_array = cls._pg_all_to_json_array(ignore=ignore)
        json_array = [] if json_array == None else json_array
        return json_array

    @classmethod
    def _manual_all_to_json_array(cls, ignore=['password', 'salt']):
        logger.debug('sqlite does not implement array_to_json()')
        users_list = []
        users = DBSession.query(cls).all()
        if users != None:
            for user in users:
                users_list.append(user._manual_to_json(ignore=ignore))
        return users_list

    @classmethod
    def _pg_all_to_json_array(cls, ignore=['password', 'salt']):
        logger.debug('execute array_to_json()')
        sql_expression = \
            """
            select array_to_json(array_agg(t)) from (
                select * from %s) t; """ % (cls.__tablename__)
        users = DBSession.execute(sql_expression).scalar()
        logger.debug('json users: %s' % users)
        if users != None:
            for user in users:
                for ig in ignore:
                    user.pop(ig)
        return users

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

    def to_json(self, request, ignore=['password', 'salt']):
        json_obj = {}
        if request.scarab_settings['backend_db'] == 'sqlite':
            json_obj = self._manual_to_json(ignore=ignore)
        elif request.scarab_settings['backend_db'] == 'postgres':
            json_obj = self._pg_row_to_json(ignore=ignore)

        logger.debug('this is json_obj: %s' % json_obj)
        json_obj = {} if json_obj == None else json_obj
        return json_obj

    def _manual_to_json(self, ignore=['password', 'salt']):
        logger.debug('sqlite does not implement row_to_json()')
        time_format = '%Y-%m-%dT%H:%M:%S%z.%f'
        user = {}
        user['user_id'] = self.user_id
        user['group_id'] = self.group_id
        user['user_name'] = self.user_name
        user['description'] = self.description
        user['activated'] = self.activated
        user['password'] = self.password
        user['salt'] = self.salt
        user['createddatetime'] = self.createddatetime.strftime(time_format)
        user['updateddatetime'] = self.updateddatetime.strftime(time_format)
        for ig in ignore:
            user.pop(ig)
        return user

    def _pg_row_to_json(self, ignore=['password', 'salt']):
        logger.debug('execute row_to_json()')
        sql_expression = \
            """
            select row_to_json(u) from (
                select *
                from %s where user_id = %s) u;
            """ % (self.__tablename__, self.user_id)
        user = DBSession.execute(sql_expression).scalar()
        logger.debug('json user: %s' % user)
        for ig in ignore:
            user.pop(ig)
        return user

