#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/12 21:04
@Author  : lex(luohai2233@163.com)

The module to parse the config file
"""
import os

import config.options as opt
from oocfg.config import exceptions


class Config(object):

    GROUP_REGISTERED = False

    def __init__(self):
        self._setup_cfg()

    def _get_config_file_type(self):
        if self.config_file.endswith('.ini'):
            return 'ini'
        elif self.config_file.endswith('.yaml'):
            return 'yaml'
        elif self.config_file.endswith('.conf'):
            return 'conf'
        else:
            raise exceptions.NoSupportType(self.config_file.split('.')[-1])

    def _load_config(self):
        conf_type = self._get_config_file_type()
        if conf_type == 'ini':
            self._load_ini_cofing()
        elif conf_type == 'yaml':
            self._load_yaml_config()
        elif conf_type == 'conf':
            self._load_conf_config()

    def _load_ini_cofing(self):
        config_map = {}
        if not os.path.exists(self.config_file):
            raise exceptions.ConfigFileNotFoundError(file=self.config_file)
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file, encoding='utf-8')

        sections = config_parser.sections()
        for section in sections:
            config_map[section] = config_parser.items(section)

        self.config_map = config_map

    def _load_yaml_config(self, cofing_file):
        self.config_map = {}

    def _load_conf_config(self, config_file):
        self.config_map = {}

    def _setup_cfg(self):
        self.CONF = opt.ConfigOpts()

    def set_default_config(self, sections):
        for group, opts in sections.items():
            self.CONF.register_opts(group.upper(), opts)
        self.GROUP_REGISTERED = True

    def load_file_config(self, config_file):
        # this method should be called after register_all_group
        self.config_file = config_file
        self._load_config()
        if not self.GROUP_REGISTERED:
            raise exceptions.GroupNoRegistered()
        self.cfg.set_config_file_value(self.config_map)


cfg = Config()

