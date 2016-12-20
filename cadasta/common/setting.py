# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSettings

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '20/12/16'
__copyright__ = 'Copyright 2016, Cadasta'


def set_setting(key, value):
    """
    Set setting
    :param key: unique key for setting
    :type key: QString
    :param value: value to be saved
    :type value: QVariant

    """
    settings = QSettings()
    settings.setValue(key, value)


def delete_setting(key):
    """
    delete setting
    :param key: unique key for setting
    :type key: QString

    """
    settings = QSettings()
    settings.remove(key)


def get_setting(key):
    """
    get setting
    :param key: unique key for setting
    :type key: QString

    :return value that saved in setting with unique key
    :rtype : QVariant
    """
    settings = QSettings()
    return settings.value(key, None)


def save_url_instance(url):
    """
    Get url that saved

    """
    set_setting("url", url)


def get_url_instance():
    """
    Get authtoken that saved
    :return authtoken that saved
    :rtype QVariant
    """
    return get_setting("url")


def save_authtoken(authtoken):
    """
    Save authtoken

    """
    set_setting("user/authtoken", authtoken)


def get_authtoken():
    """
    Get authtoken that saved
    :return authtoken that saved
    :rtype QVariant
    """
    return get_setting("user/authtoken")
