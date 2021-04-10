#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/12 21:04
@Author  : lex(luohai2233@163.com)

The module to parse the config file
"""

import exceptions


class Opt(object):
    def __init__(self, name, default=None, helper=None, alias=None, current=None):
        self.name = name
        self.helper = helper

        self._validate(default)
        self.default = default

        if alias is None:
            self.alias = self.name.replace('-', '_')
        else:
            self.alias = alias
        self.current = None
        if current is not None:
            self._validate(current)
            self._convert_and_set_current(current)

    def _vars_for_cmp(self):
        v = dict(vars(self))
        return v

    def __ne__(self, another):
        return self._vars_for_cmp() != another._vars_for_cmp()

    def __eq__(self, another):
        return self._vars_for_cmp() == another._vars_for_cmp()

    def convert_and_set_current(self, current):
        raise NotImplementedError

    def _validate(self, current):
        # just use to validate the given value, raise exception if error
        # if all is well return True
        raise NotImplementedError

    def _default_is_ref(self):
        """Check if default is a reference to another var."""
        if isinstance(self.default, str):
            tmpl = self.default.replace(r'\$', '').replace('$$', '')
            return '$' in tmpl
        return False


class StrOpt(Opt):
    def __init__(self, name, choices=None, **kwargs):
        self.choices = choices
        super(StrOpt, self).__init__(name, **kwargs)

    def _get_choice_text(self, choice):
        if choice is None:
            return '<None>'
        elif choice == '':
            return ''
        else:
            return str(choice)

    def _validate(self, current):
        if self.choices is not None:
            if current not in self.choices:
                raise exceptions.NoSuchChoiceError(name=self.name, choices=self.choices, current=current)

    def convert_and_set_current(self, current):
        """the default type of value from config.ini string, so we do noting"""
        self._validate(current)
        self.current = current


class ListOpt(Opt):
    def __init__(self, **kwargs):
        super(ListOpt, self).__init__( **kwargs)

    def _validate(self, current):
        if not isinstance(current, list):
            raise exceptions.ListTypeError(name=self.name)

    def convert_and_set_current(self, current):
        tmp = current.split(",")
        current_value = []
        for cur in tmp:
            if tmp == ' ':
                continue

            # we just convert all the list value to string type
            current_value.append(str(cur))
        self.current = current_value


class BoolOpt(Opt):
    TRUE_VALUES = ['true', '1', 'yes', 'on']
    FALSE_VAULES = ['false', '0', 'no', 'off']

    def __init__(self,  **kwargs):
        super(BoolOpt, self).__init__(**kwargs)

    def _validate(self, current):
        if current.lower() not in self.TRUE_VALUES or current.lower() not in self.FALSE_VAULES:
            raise exceptions.BoolOptError(name=self.name)

    def convert_and_set_current(self, current):
        if current.lower in self.TRUE_VALUES:
            self.current = True
        else:
            self.current = False


class IntOpt(Opt):
    def __init__(self, name, **kwargs):
        super(IntOpt, self).__init__(name, **kwargs)

    def _validate(self, current):
        int(current)

    def convert_and_set_current(self, current):
        self.current = int(current)


class FloatOpt(Opt):
    def __init__(self, **kwargs):
        super(FloatOpt, self).__init__(**kwargs)

    def _validate(self, current):
        float(current)

    def convert_and_set_current(self, current):
        self.current = float(current)


class GroupOpt(object):
    def __init__(self, name):
        self.name = name
        self._opts = {}

    def _register_opt(self, opt):
        """
        regist an opt to this group
        :param opt: an object of Opt
        :return:
        """
        if _is_opt_registered(self._opts, opt):
            return False

        self._opts[opt.alias] = {'opt': opt}
        return True

    def _unregister_opt(self, opt):
        if opt.alias in self._opts:
            del self._opts[opt.alias]

    def register_opts(self, opts):
        for opt in opts:
            self._register_opt(opt)

    def clear(self):
        self._opts = {}

    def __getitem__(self, opt):
        if opt not in self._opts:
            raise exceptions.NoSuchOpt(opt)

        return self._get_current_or_default(self._opts[opt]['opt'])

    def _get_current_or_default(self, opt):
        if opt.current is not None:
            return opt.current
        return opt.default

    def set_opt_value(self, opt, current):
        self._opts[opt]['opt'].convert_and_set_current(current)

    def __getattr__(self, opt):
        return self.__getitem__(opt)


class ConfigOpts(object):
    def __init__(self):
        self._group = {}

    def set_config_file_value(self, config_map):
        for group, opts in config_map.items():
            registered_group = self._get_group(group, from_file=True)
            for opt_name, opt_value in opts.items():
                registered_group.set_opt_value(opt_name, opt_value)

    def register_opts(self, group, opts):
        registered_group = self._get_group(group)
        registered_group.register_opts(opts)

    def _get_group(self, group, from_file=False):
        if not from_file:
            return self.register_group_if_not_exist(group)
        else:
            return self._group[group]

    def register_group_if_not_exist(self, group):
        if group not in self._group:
            self._group[group] = GroupOpt(group)
        return self._group[group]

    def __getitem__(self, group):
        if group not in self._group:
            raise exceptions.NoSuchGroup("No such group %s" % group)
        return self._group.get(group)

    def __getattr__(self, group):
        return self.__getitem__(group)


def _is_opt_registered(opts, opt):
    """Check whether an opt with the same name is already registered.

    The same opt may be registered multiple times, with only the first
    registration having any effect. However, it is an error to attempt
    to register a different opt with the same name.

    :param opts: the set of opts already registered
    :param opt: the opt to be registered
    :returns: True if the opt was previously registered, False otherwise
    :raises: DuplicateOptError if a naming conflict is detected
    """
    if opt.alias in opts:
        if opts[opt.alias]['opt'] != opt:
            raise exceptions.DuplicateOptError(opt.name)
        return True
    else:
        return False
