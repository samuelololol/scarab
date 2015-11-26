#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Oct 23, 2015 '
__author__= 'samuel'
import random
import string
import codecs
import os
import ConfigParser
import io
import sys

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def db_config(key):
    config_path = os.path.dirname(__file__)    # test/common
    config_path = os.path.dirname(config_path) # scarab/test
    config_path = os.path.dirname(config_path) # scarab/scarab
    config_path = os.path.dirname(config_path) # scarab
    config_path = os.path.join(config_path, 'development.ini') #scarab/development.ini
    with open(config_path, 'r') as f:
        config_content = f.read()
    if sys.version_info[0:2] == (2,6):
        config = ConfigParser.RawConfigParser()
    else:
        config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(config_content))
    DB_URL = config.get('app:main', key)
    return DB_URL

