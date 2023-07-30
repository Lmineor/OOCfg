#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author  : lex(luohai2233@163.com)
"""
import os

import configparser
import yaml

from src.config import exceptions


def get_config_file_type(config_file):
    if config_file.endswith('.ini'):
        return 'ini'
    elif config_file.endswith('.yaml'):
        return 'yaml'
    elif config_file.endswith('.conf'):
        return 'conf'
    else:
        raise exceptions.NoSupportType(config_file.split('.')[-1])


def load_ini_cofing(config_file):
    config_map = {}
    if not os.path.exists(config_file):
        raise exceptions.ConfigFileNotFoundError(file=config_file)
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file, encoding='utf-8')

    sections = config_parser.sections()
    for section in sections:
        config_map[section] = config_parser.items(section)
    return config_map


def load_yaml_config(config_file):
    config = []
    if not os.path.exists(config_file):
        raise exceptions.ConfigFileNotFoundError(file=config_file)
    with open(config_file, 'r', encoding='utf-8') as ymlfile:
        cfgs = yaml.load_all(ymlfile, Loader=yaml.SafeLoader)
        for cfg in cfgs:
            config.append(cfg)

    if len(config) > 1:
        raise exceptions.MultiGroupNotSupport
    return config[0] if config else {}


def load_conf_config(config_file):
    return load_ini_cofing(config_file)
