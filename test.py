#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author  : lex(luohai2233@163.com)
"""

from oocfg import cfg
from oocfg import options

info_opts = [
    options.StrOpt('name', default='xiao', helper='this is name config'),
    options.IntOpt('age', default=18, helper='this is age config'),
    options.StrOpt('sex', default='female', helper='this is gender config', choices=['female', 'male']),
    options.ListOpt('car', default=[], helper='cars num'),
    options.BoolOpt('sexy', default=True, helper='is sexy?'),
    options.FloatOpt('pi', default=3.14, helper="pi")
]

class_opts = [
    options.IntOpt('class', default='6', helper='the class grade'),
    options.StrOpt('school', default='xi wang xiao xue', helper='school name')
]

group = {
    'class': class_opts,
    'info': info_opts
}


def test_default_config():
    cfg.startup(group)
    print(cfg.CONF.CLASS.school)


def test_load_yaml():
    file = '/Users/lex/code/coding/OOCfg/test_file/config.yaml'
    from oocfg.config.utils import load_yaml_config
    print(load_yaml_config(file))


def test_yaml_config():
    file = '/Users/lex/code/coding/OOCfg/test_file/config.yaml'
    cfg.startup(group, config_file=file)
    print(cfg.CONF.CLASS.school)
    print(cfg.CONF.INFO.car)
    print(cfg.CONF.INFO.sexy)


def test_ini_config():
    file = '/Users/lex/code/coding/OOCfg/test_file/config.ini'
    cfg.startup(group, config_file=file)
    print(cfg.CONF.CLASS.school)
    print(cfg.CONF.INFO.car)
    print(cfg.CONF.INFO.sexy)


def test_conf_config():
    file = '/Users/lex/code/coding/OOCfg/test_file/config.conf'
    cfg.startup(group, config_file=file)
    print(cfg.CONF.CLASS.school)
    print(cfg.CONF.INFO.car)
    print(cfg.CONF.INFO.sexy)
    print(cfg.CONF.INFO.pi)


if __name__ == '__main__':
    test_default_config()
    # test_load_yaml()
    test_yaml_cofing()
    test_ini_config()
    test_conf_config()
