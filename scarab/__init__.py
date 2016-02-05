#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy import event

from scarab.routes import api_routes

from scarab.models import (
    DBSession,
    Base,
    )

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid_multiauth import MultiAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from scarab.security import get_user
from scarab.security import groupfinder

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_key=ON')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    global DBSession, Base
    engine = engine_from_config(settings, 'sqlalchemy.')

    backend_db = 'sqlite' if 'sqlite://' in settings['sqlalchemy.url'] else 'postgres'
    scarab_settings = {}
    scarab_settings['backend_db'] = backend_db
    logger.debug('scarab_settings: %s' % scarab_settings)
    def get_scarab_settings(request):
        return scarab_settings

    #enable sqlite foreignkey if sqlite
    if 'sqlite' == backend_db:
        event.listen(engine, 'connect', _fk_pragma_on_connect) #db foreignkey on
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine


    config = Configurator(root_factory='scarab.models.RootFactory', settings=settings)
    #api routes
    config.include(api_routes)

    #embeded userojb to request
    config.add_request_method(get_user, 'user', reify=True)
    config.add_request_method(get_scarab_settings, 'scarab_settings', reify=True)

    #security; add policies here
    policies =[AuthTktAuthenticationPolicy(settings['scarab.auth_secret'],
                                           callback=groupfinder,
                                           hashalg='sha512')]
    authn_policy = MultiAuthenticationPolicy(policies)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    #all setting is done, scan config
    config.scan()
    return config.make_wsgi_app()

