# -*- coding: utf-8 -*-
"""
Cadasta project - **Login api.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
from qgis.PyQt.QtCore import QByteArray
from cadasta.mixin.network_mixin import NetworkMixin

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '16/12/16'
__copyright__ = 'Copyright 2016, Cadasta'


class Login(NetworkMixin):
    def __init__(self, domain, username, password, on_finished=None):
        """
        Constructor.
        :param username:
        :param password:
        :param on_finished: is a function that catch tools result request
        :return:
        """
        self.request_url = domain + 'api/v1/account/login/?'
        super(Login, self).__init__()
        post_data = QByteArray()
        post_data.append("username=%s&" % username)
        post_data.append("password=%s" % password)

        self.connect_post(post_data)
        self.on_finished = on_finished

    def connection_finished(self):
        """On finished function when tools request is finished."""
        # extract result
        if self.error:
            self.on_finished(self.error)
        else:
            result = self.get_json_results()
            if self.on_finished and callable(self.on_finished):
                self.on_finished(result)
