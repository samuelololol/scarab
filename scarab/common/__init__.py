#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Nov 21, 2015 '
__author__= 'samuel'

import inspect
import traceback

def ModelMethod(src_logger):
    def wrap(func):
        def wrapped_func(cls, *args, **kwargs):
            try:
                rtn = func(cls, *args, **kwargs)
            except Exception, e:
                rtn = twin_tuple_rtn(
                        exp=e,
                        ins_stk=inspect.stack()[0][3],
                        tbk=traceback.format_exc(),
                        logger=src_logger,
                        err_src = cls.__tablename__,
                        )
            return rtn
        return  wrapped_func
    return wrap


def twin_tuple_rtn(exp, ins_stk, tbk, logger, err_src=None):
    rtn = []
    err_info = (err_src, ins_stk, tbk)
    logger.error('%s:%s, traceback:\n %s' % err_info, exc_info=True)

    #rtn is twin tuple: (False, {})
    rtn.append(False)
    rtn.append({'status':'fail', 'msg':'%s error on %s' % (err_src, ins_stk)})
    return rtn

