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
    __tablename__ = 'group'

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
    __tablename__ = 'user'

    user_id         = Column(Integer,      nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_name       = Column(Unicode(255), nullable=False, unique=True, index=True)
    description     = Column(Unicode(255), nullable=True,  unique=False)
    activated       = Column(Boolean,      nullable=False, unique=False)
    password        = Column(String(255),  nullable=False, unique=False)
    salt            = Column(String(255),  nullable=False, unique=False)
    createddatetime = Column(DateTime,     nullable=False)
    updateddatetime = Column(DateTime,     nullable=False)

    #fk
    group_id      = Column(Integer, ForeignKey('group.group_id'), nullable=False, unique=False)

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

    def pwd_validate(self, name, password):
        test_pwd = hashlib.sha512(self.salt + password).hexdigest()

        result = 0
        db_pass_len = len(self.password)
        test_pass_len = len(test_pwd)
        result = db_pass_len ^ test_pass_len
        if result != 0:
            return (False, 'password incorrect.')

        for i in xrange(db_pass_len):
            result += (ord(test_pwd[i]) ^ ord(self.password[i]))

        if result == 0:
            return (True, 'password is correct')
        else:
            return (False, 'password is incorrect.')

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


