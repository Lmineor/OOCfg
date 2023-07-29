#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/12 21:04
@Author  : lex(luohai2233@163.com)

The module to parse the config file
"""
from typing import List, Dict, Any

from oocfg.config import exceptions


class Opt(object):
    """
    Opt standard for a config option
    """

    def __init__(self, name: str, default=None, helper='', alias=None, current=None):
        self.name = name.replace(" ", "")
        self.helper = helper

        default = self._validate(default)
        self.default = default

        if alias is None:
            self.alias = self.name.replace('-', '_')
        else:
            self.alias = alias
        self.current = None
        if current is not None:
            self._validate(current)
            self.convert_and_set_current(current)

    def _vars_for_cmp(self):
        v = dict(vars(self))
        return v

    def __ne__(self, another: Any):
        return self._vars_for_cmp() != another._vars_for_cmp()

    def __eq__(self, another: Any):
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

    @property
    def value(self):
        if self.current is not None:
            return self.current
        return self.default

    def __str__(self):
        return "<name: %(name)s, value %(value)s>" % {"name": self.name, "value": self.value}

    def __repr__(self):
        return self.__str__()


class StrOpt(Opt):
    def __init__(self, name: str, choices: List[str] = None, **kwargs):
        self.choices = self.validate_and_optimize_choices(choices)
        super(StrOpt, self).__init__(name, **kwargs)

    @staticmethod
    def validate_and_optimize_choices(choices: List[str]):
        if choices is None:
            # does not provide choices
            return
        if not isinstance(choices, list):
            raise exceptions.ChoicesTypeError
        parsed = list()
        for choice in choices:
            parsed.append(choice.replace(" ", ""))
        return parsed

    @staticmethod
    def _get_choice_text(choice: str):
        if not choice:
            return '<None>'
        elif choice == '':
            return ''
        else:
            return str(choice)

    def _validate(self, value: str) -> str:
        value = value.replace(" ", "")
        if self.choices:
            if value not in self.choices:
                raise exceptions.NoSuchChoiceError(name=self.name, choices=self.choices, current=value)
        return value

    def convert_and_set_current(self, current: str):
        """the default type of value from config.ini string, so we do nothing"""
        self._validate(current)
        self.current = current.replace(" ", "")


class ListOpt(Opt):
    def __init__(self, name: str, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = list()
        super(ListOpt, self).__init__(name, **kwargs)

    def _validate(self, value: List[str]) -> List:
        if not isinstance(value, list):
            raise exceptions.ListTypeError(name=self.name)
        return value

    def convert_and_set_current(self, current: str):
        if isinstance(current, list):
            tmp = current
        else:
            tmp = current.replace(" ", "").split(",")

        current_value = []
        for cur in tmp:
            # we just convert all the list value to string type
            current_value.append(str(cur))
        self.current = current_value


class BoolOpt(Opt):
    true_values = ['true', '1', 'yes', 'on']
    false_values = ['false', '0', 'no', 'off']

    def __init__(self, name: str, **kwargs):
        super(BoolOpt, self).__init__(name, **kwargs)

    def _validate(self, value: Any):
        if isinstance(value, bool):
            return value
        value = str(str(value).replace(" ", "")).lower()
        if not (value in self.true_values or value in self.false_values):
            raise exceptions.BoolOptError(name=self.name)
        if value in self.true_values:
            return True
        else:
            return False

    def convert_and_set_current(self, current: Any):
        if isinstance(current, bool):
            self.current = current
            return
        current = str(current).replace(" ", "")
        if str(current).lower() in self.true_values:
            self.current = True
        else:
            self.current = False


class IntOpt(Opt):
    def __init__(self, name: str, **kwargs: object):
        super(IntOpt, self).__init__(name, **kwargs)

    def _validate(self, current):
        return int(current)

    def convert_and_set_current(self, current):
        self.current = int(current)


class FloatOpt(Opt):
    def __init__(self, name, **kwargs):
        super(FloatOpt, self).__init__(name, **kwargs)

    def _validate(self, current):
        return float(current)

    def convert_and_set_current(self, current):
        self.current = float(current)


class GroupOpt(object):
    def __init__(self, name: str):
        name = name.replace(" ", "")
        self.name = name

        self._opts = {}  # {alias: Opt}

    def _register_opt(self, opt: Opt) -> bool:
        """
        register an opt to this group
        :param opt: an object of Opt
        :return:
        """
        if _is_opt_registered(self._opts, opt):
            return False

        self._opts[opt.alias] = opt
        return True

    def _unregister_opt(self, opt):
        if opt.alias in self._opts:
            del self._opts[opt.alias]

    def register_opts(self, opts: List[Opt]):
        for opt in opts:
            self._register_opt(opt)

    def clear(self):
        self._opts = {}

    def set_opt_value(self, opt: str, current: Any):
        self._opts[opt].convert_and_set_current(current)

    def __getattr__(self, opt: Opt):
        return self.__getitem__(opt)

    def __getitem__(self, opt: Opt):
        if opt not in self._opts:
            raise exceptions.NoSuchOpt(opt)

        return self._opts[opt].value

    def __str__(self):
        return self.name.upper()

    def __repr__(self):
        return self.__str__()


class ConfigOpts(object):
    def __init__(self):
        self._group = {}

    def set_config_file_value(self, config_map: Dict[str, Dict[str, str]]):
        for group, opts in config_map.items():
            registered_group = self._get_group(group, from_file=True)
            if not isinstance(opts, dict):
                opts = dict(opts)
            for opt_name, opt_value in opts.items():
                registered_group.set_opt_value(opt_name, opt_value)

    def register_opts(self, group: str, opts):
        registered_group = self._get_group(group)
        registered_group.register_opts(opts)

    def _get_group(self, group: str, from_file=False) -> GroupOpt:
        group = group.replace(" ", "").upper()
        if not from_file:
            return self.register_group_if_not_exist(group)
        else:
            return self._group[group]

    def register_group_if_not_exist(self, group: str) -> GroupOpt:

        if group not in self._group:
            self._group[group] = GroupOpt(group)
        return self._group[group]

    def __getitem__(self, group) -> GroupOpt:
        group = group.replace(" ", "").upper()
        if group not in self._group:
            raise exceptions.NoSuchGroup("No such Group %s" % group)
        return self._group[group]

    def __getattr__(self, group):
        return self.__getitem__(group)


def _is_opt_registered(opts: Dict[str, Opt], opt: Opt):
    """Check whether an opt with the same name is already registered.

    The same opt may be registered multiple times, with only the first
    registration having any effect. However, it is an error to attempt
    to register a different opt with the same name.

    :param opts: the set of opts already registered
    :param opt: opt to be registered
    :returns: True if opt was previously registered, False otherwise
    :raises: DuplicateOptError if a naming conflict is detected
    """
    if opt.alias in opts:
        if opts[opt.alias] != opt:
            raise exceptions.DuplicateOptError(opt=opt.name)
        return True
    else:
        return False
