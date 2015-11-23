#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 24, 2015 '
__author__= 'samuel'

import logging
#class NullHandler(logging.Handler):
#    def emit(self, record):
#        pass
#logging.getLogger().addHandler(NullHandler())

#h = logging.StreamHandler()
#h.setLevel(logging.DEBUG)
FORMAT = "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logging.getLogger().addHandler(logging.StreamHandler())
