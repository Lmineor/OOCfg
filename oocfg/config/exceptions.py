#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author  : lex(luohai2233@163.com)
"""


class OOCfgException(Exception):
    """
    Base exception for oocfg
    """
    message = "This is the base exception"

    def __init__(self, **kwargs):
        self.message = self.message % kwargs

    def __str__(self):
        return self.message


class NoSuchChoiceError(OOCfgException):
    message = "Option %(name)s value should be in %(choices)s, You give %(current)s ."


class ListTypeError(OOCfgException):
    message = "Option %(name)s value's type should be a type of List!"


class BoolOptError(OOCfgException):
    message = "Option %(name)s value's type should be a type of Bool!"


class ConfigFileNotFoundError(OOCfgException):
    message = "Config file %(file)s does not exist, Please check it!"


class DuplicateOptError(OOCfgException):
    message = "Duplicate Opt Error for %s!"


class DefaultValueError(OOCfgException):
    def __init__(self, msg):
        self.message = msg


class NoSuchGroup(OOCfgException):
    def __init__(self, msg):
        self.message = msg


class NoSuchOpt(OOCfgException):
    def __init__(self, opt):
        self.message = "No such opt %s error!" % opt


class GroupNoRegistered(OOCfgException):
    message = "Not all Group has registered!"


class NoSupportType(OOCfgException):
    def __init__(self, type_):
        self.message = "This type %s does not support." % type_


class MultiGroupNotSupport(OOCfgException):
    message = "Multi Group Not Support!"


class EmptySections(OOCfgException):
    message = "Empty Sections."


class SectionsFormatError(OOCfgException):
    message = "sections should be a format of dict."


class OptsFormatError(OOCfgException):
    message = "Opts Format Error!"
