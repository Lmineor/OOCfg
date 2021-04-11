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
from config import utils


class Config(object):

    GROUP_REGISTERED = False

    def __init__(self):
        self.config_file = None
        self._setup_cfg()

    def _setup_cfg(self):
        self.CONF = opt.ConfigOpts()

    def _load_config_file(self):
        conf_type = utils.get_config_file_type(self.config_file)
        if conf_type == 'ini':
            self.config_map = utils.load_ini_cofing(self.config_file)
        elif conf_type == 'yaml':
            self.config_map = utils.load_yaml_config(self.config_file)
        elif conf_type == 'conf':
            self.config_map = utils.load_conf_config(self.config_file)

    def set_default_config(self, sections):
        """
        set default config value.
        After the default config value, we can override the config with config file.
        This is import because all the config load from config file
        will work after this method
        :param sections:
        :return:
        """
        for group, opts in sections.items():
            self.CONF.register_opts(group.upper(), opts)
        self.GROUP_REGISTERED = True

    def startup(self, sections, config_file=None, auto_find=False):
        """
        main method of load config file
        :param config_file: the absolute path of config_file, like, /etc/project/config.ini
        :param sections: the default config group to register
        :param auto_find: if config_file is None, whether to find config file
        :return:
        """
        self.set_default_config(sections)

        # this method should be called after register_all_group
        if config_file is None and not auto_find:
            # the default config value is enough
            return
        self.config_file = config_file
        self._load_config_file()
        if not self.GROUP_REGISTERED:
            raise exceptions.GroupNoRegistered()
        self.CONF.set_config_file_value(self.config_map)


cfg = Config()

