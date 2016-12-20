# -*- coding: utf-8 -*-
"""
Cadasta project - **Setting utilities**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
from qgis.PyQt.QtCore import QSettings

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '20/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

default_domain = 'https://demo.cadasta.org/'


def set_setting(key, value):
    """
    Set setting.
    :param key: unique key for setting
    :type key: QString
    :param value: value to be saved
    :type value: QVariant

    """
    settings = QSettings()
    settings.setValue(key, value)


def delete_setting(key):
    """
    delete setting.
    :param key: unique key for setting
    :type key: QString

    """
    settings = QSettings()
    settings.remove(key)


def get_setting(key):
    """
    get setting.
    :param key: unique key for setting
    :type key: QString

    :return value that saved in setting with unique key
    :rtype : QVariant
    """
    settings = QSettings()
    return settings.value(key, None)


def save_url_instance(url):
    """
    Save url instance that received.
    :param url: url instance that will saved
    :type url: QString

    """
    set_setting("url", url)


def get_url_instance():
    """
    Get url instance that saved.
    :return url instance that saved
    :rtype QVariant
    """
    settings = QSettings()
    return settings.value(
        "url",
        default_domain
    )


def delete_url_instance():
    """
    Delete url instance that saved.

    """
    delete_setting("url")


def save_authtoken(authtoken):
    """
    Save authtoken.
    :param authtoken: authtoken that will saved
    :type authtoken: QString

    """
    set_setting("user/authtoken", authtoken)


def get_authtoken():
    """
    Get authtoken that saved.
    :return authtoken that saved
    :rtype QVariant
    """
    return get_setting("user/authtoken")


def delete_authtoken():
    """
    Delete authtoken that saved.

    """
    delete_setting("user/authtoken")
