import logging
logger = logging.getLogger(__name__)

import os
import sys
import transaction

from sqlalchemy import engine_from_config
from pyramid.scripts.common import parse_vars

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    )

from ..models.mymodel import MyModel
from ..models.account import Group_TB
from ..models.account import User_TB


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def initialization(Base, DBSession, engine, drop_all=True):
    #clean up
    with transaction.manager:
        if drop_all:
            Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    with transaction.manager:
        model = MyModel(name='one', value=1)
        DBSession.add(model)
        DBSession.flush()

        group_model = Group_TB(group_name=u'public', description=u'Public Group')
        DBSession.add(group_model)
        DBSession.flush()

        success, user_model = User_TB.create(user_name=u'public',
                                             description=u'Public User',
                                             password=u'12345678',
                                             activated=True,
                                             group_id=group_model.group_id
                                             )
        DBSession.flush()



def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    initialization(Base=Base, DBSession=DBSession, engine=engine)
    logger.info('DB initialization done.')






    ##template example
    #with transaction.manager:
    #    model = MyModel(name='one', value=1)
    #    DBSession.add(model)

    #with transaction.manager:
    #    """
    #    user SQLAlchemy ORM object to create group instance
    #    """
    #    group_model = Group_TB(group_name=u'public', description=u'Public Group')
    #    DBSession.add(group_model)

    #with transaction.manager:
    #    """
    #    use custom model method to create user instance
    #    """
    #    success, user_model = User_TB.create(user_name=u'public', description=u'Public User',
    #                                         password=u'12345678', activated=True,
    #                                         group_id=group_model.group_id)
    #    if not success: raise Exception(user_model)

