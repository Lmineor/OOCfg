#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author  : lex(luohai2233@163.com)
"""

from oocfg.cfg import cfg
from oocfg.config import options

info_opts = [
    options.StrOpt('name', default='xiao', helper='this is name config'),
    options.IntOpt('age', default=18, helper='this is age config'),
    options.StrOpt('sex', default='female', helper='this is gender config', choices=['female', 'male'])
]

class_opts = [
    options.IntOpt('class', default='6', helper='the class grade'),
    options.StrOpt('school', default='xi wang xiao xue', helper='school name')
]

group = {
    'class': class_opts,
    'info': info_opts
}


cfg.set_default_config(group)

print(cfg.CONF.CLASS.school)
# cfg.load_file_config()