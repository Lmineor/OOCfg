#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author  : lex(luohai2233@163.com)
"""
import os

import pytest

from oocfg import cfg
from oocfg import options

from oocfg.config import exceptions


def test_str_opt():
    with pytest.raises(expected_exception=exceptions.ChoicesTypeError):
        options.StrOpt('name', default='abc', current='bcd  ', choices='a', helper='this is name config')

    with pytest.raises(expected_exception=exceptions.NoSuchChoiceError):
        options.StrOpt('name', default='abc', current='bcd', choices=['b'], helper='this is name config')

    opt = options.StrOpt('na me', default=' abc', current='bc d ', helper='this is name config')
    assert opt.name == "name"
    assert opt.default == "abc"
    assert opt.value == "bcd"

    opt = options.StrOpt('na me', default=' abc', current='bc d ', choices=["abc", "bcd   "],
                         helper='this is name config')
    assert opt.name == "name"
    assert opt.default == "abc"
    assert opt.value == "bcd"

    opt = options.StrOpt('name', default='abc', current='bcd ', choices=["abc", "bcd"],
                         helper='this is name config')
    assert opt.name == "name"
    assert opt.default == "abc"
    assert opt.value == "bcd"

    opt = options.StrOpt('name', default='abc', current=' ',
                         helper='this is name config')
    assert opt.name == "name"
    assert opt.default == "abc"
    assert opt.value == ""

def test_int_opt():
    with pytest.raises(ValueError):
        options.IntOpt('age', default='a18', helper='this is age config')

    opt = options.IntOpt('age', default=18, helper='this is age config')
    assert opt.value == 18
    assert opt.default == 18

    opt = options.IntOpt('ag e', default=18, current=19, helper='this is age config')
    assert opt.name == 'age'
    assert opt.value == 19
    assert opt.default == 18
    assert opt.helper == 'this is age config'


def test_bool_opt():
    with pytest.raises(exceptions.BoolOptError):
        options.BoolOpt('ok', default='a18', helper='this is ok config')
    opt = options.BoolOpt('o k', default='1', helper='this is ok config')
    assert opt.name == 'ok'
    assert opt.value

    opt = options.BoolOpt('ok', default='0', helper='this is ok config')
    assert opt.name == 'ok'
    assert not opt.value

    opt = options.BoolOpt('ok', default='0', current=1, helper='this is ok config')
    assert opt.name == 'ok'
    assert opt.value

    opt = options.BoolOpt('ok', default='1', current=0, helper='this is ok config')
    assert opt.name == 'ok'
    assert not opt.value

    opt = options.BoolOpt('ok', default=True, current=1, helper='this is ok config')
    assert opt.name == 'ok'
    assert opt.value

    opt = options.BoolOpt('ok', default=False, current=0, helper='this is ok config')
    assert opt.name == 'ok'
    assert not opt.value

    opt = options.BoolOpt('ok', default=True, current=False, helper='this is ok config')
    assert opt.name == 'ok'
    assert not opt.value

    opt = options.BoolOpt('ok', default=False, current=True, helper='this is ok config')
    assert opt.name == 'ok'
    assert opt.value


def test_list_opt():
    with pytest.raises(exceptions.ListTypeError):
        options.ListOpt('car', default='', helper='cars num')
    opt = options.ListOpt('car', default=[], helper='cars num')
    assert opt.value == []

    opt = options.ListOpt('car', default=['car'], helper='cars num')
    assert opt.value == ['car']

    opt = options.ListOpt('car', default=['car'], current=['car1'], helper='cars num')
    assert opt.value == ['car1']
    assert opt.default == ['car']


# info_opts = [
#     options.StrOpt('name', default='xiao', helper='this is name config'),
#     options.IntOpt('age', default=18, helper='this is age config'),
#     options.StrOpt('sex', default='female', helper='this is gender config', choices=['female', 'male']),
#     options.ListOpt('car', default=[], helper='cars num'),
#     options.BoolOpt('sexy', default=True, helper='is sexy?'),
#     options.FloatOpt('pi', default=3.14, helper="pi")
# ]
#
# class_opts = [
#     options.IntOpt('class', default='6', helper='the class grade'),
#     options.StrOpt('school', default='xi wang xiao xue', helper='school name')
# ]
#
# group = {
#     'class': class_opts,
#     'info': info_opts
# }
#
#
# def get_env_file(typ):
#     if typ == 'ini':
#         return os.environ['OO_FILE_INI']
#     elif typ == 'yaml':
#         return os.environ['OO_FILE_YAML']
#     elif typ == "conf":
#         return os.environ['OO_FILE_CONF']
#     else:
#         raise Exception("please provide configuration file")
#
#
# def test_default_config():
#
#     cfg.startup(group)
#     print(cfg.CONF.CLASS.school)
#
#
# def test_load_yaml():
#     file = get_env_file('yaml')
#     from oocfg.config.utils import load_yaml_config
#     print(load_yaml_config(file))
#
#
# def test_yaml_config():
#     file = get_env_file('yaml')
#     cfg.startup(group, config_file=file)
#     print(cfg.CONF.CLASS.school)
#     print(cfg.CONF.INFO.car)
#     print(cfg.CONF.INFO.sexy)
#
#
# def test_ini_config():
#     file = get_env_file('ini')
#     cfg.startup(group, config_file=file)
#     print(cfg.CONF.CLASS.school)
#     print(cfg.CONF.INFO.car)
#     print(cfg.CONF.INFO.sexy)
#
#
# def test_conf_config():
#     file = get_env_file('conf')
#     cfg.startup(group, config_file=file)
#     print(cfg.CONF.CLASS.school)
#     print(cfg.CONF.INFO.car)
#     print(cfg.CONF.INFO.sexy)
#     print(cfg.CONF.INFO.pi)
#
#
# if __name__ == '__main__':
#     # test_default_config()
#     # test_load_yaml()
#     test_yaml_config()
#     # test_ini_config()
#     # test_conf_config()
