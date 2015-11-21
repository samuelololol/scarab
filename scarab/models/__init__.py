 #!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 21, 2015 '
__author__= 'samuel'

import logging
log = logging.getLogger(__name__)

#resource tree, rootfactory
from pyramid.security import (
        Allow,
        Everyone,
        Authenticated,
        )

from zope.sqlalchemy import ZopeTransactionExtension as ZTE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
        scoped_session,
        sessionmaker,
      )

Base = declarative_base()
#DBSession = scoped_session(sessionmaker(expire_on_commit=False, extension=ZTE(keep_session=False)))
DBSession = scoped_session(sessionmaker(extension=ZTE(keep_session=True)))


class RootFactory(object):
    __name__ = None
    __parent__ = None
    __acl__ = [
                (Allow, Everyone, 'view'),
                (Allow, Authenticated, 'login'),
            ]

    def __init__(self, request):
        self.reques=request

