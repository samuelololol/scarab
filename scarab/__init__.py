#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy import event

from scarab.routes import api_routes

from scarab.models import (
    DBSession,
    Base,
    )

from scarab.security import get_user
from scarab.security import groupfinder

#security
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_key=ON')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    global DBSession, Base
    engine = engine_from_config(settings, 'sqlalchemy.')

    scarab_settings = {}
    scarab_settings['backend_db'] = settings['backend_db']
    def get_luwak_settings(request):
        return scarab_settings

    #enable sqlite foreignkey if sqlite
    if 'sqlite' == settings['backend_db']:
        event.listen(engine, 'connect', _fk_pragma_on_connect) #db foreignkey on
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine


    config = Configurator(root_factory='scarab.models.RootFactory', settings=settings)
    #api routes
    api_routes(config)
    #security
    authn_policy = AuthTktAuthenticationPolicy(settings['scarab.auth_secret'], callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    #embeded userojb to request
    config.add_request_method(get_user, 'user', reify=True)
    config.add_request_method(get_luwak_settings, 'scarab_settings', reify=True)

    #all setting is done, scan config
    config.scan()
    return config.make_wsgi_app()

