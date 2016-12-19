# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CadastaDialog
                                 A QGIS plugin
 This tool helps create, update, upload and download Cadasta projects.
                             -------------------
        begin                : 2016-11-25
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Kartoza
        email                : christian@kartoza.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import logging
from qgis.PyQt import QtGui
from qgis.gui import QgsMessageBar
from cadasta.utilities.resources import get_ui_class

from cadasta.api.login import Login

LOGGER = logging.getLogger('CadastaQGISPlugin')
FORM_CLASS = get_ui_class('cadasta_login_base.ui')


class CadastaLogin(QtGui.QDialog, FORM_CLASS):
    def button_style(self):
        return "color:white; border-radius: 5px;"

    def __init__(self, parent=None):
        """Constructor."""
        super(CadastaLogin, self).__init__(parent)
        self.setupUi(self)
        self.msg_bar = None
        self.text_test_connection_button = self.test_connection_button.text()
        self.ok_label.setVisible(False)
        self.init_style()

    def init_style(self):
        self.setStyleSheet("background-color:white")
        self.disable_button(self.save_button)
        self.enable_button(self.test_connection_button)
        self.test_connection_button.clicked.connect(self.login)

    def enable_button(self, custom_button):
        """Enable button"""
        custom_button.setEnabled(True)
        custom_button.setStyleSheet("background-color:#525252; cursor:pointer;" + self.button_style())

    def disable_button(self, custom_button):
        """Disable button"""
        custom_button.setStyleSheet("background-color:#A8A8A8;" + self.button_style())
        custom_button.setEnabled(False)

    def login(self):
        """Login function when tools button clicked"""
        username = self.username_input.displayText()
        password = self.password_input.text()
        url = self.url_input.displayText()

        self.disable_button(self.save_button)
        self.ok_label.setVisible(False)

        if not url or not username or not password:
            self.msg_bar = QgsMessageBar()
            self.msg_bar.pushWarning("Error", "URL/Username/password is empty.")
        else:
            self.disable_button(self.test_connection_button)
            self.test_connection_button.setText("logging in")
            # call tools API
            self.login_api = Login(url, username, password, self.on_finished)

    def on_finished(self, result):
        self.ok_label.setVisible(True)
        """On finished function when tools request is finished"""
        if 'auth_token' in result:
            auth_token = result['auth_token']
            output_result = "auth_token is %s" % auth_token
            self.enable_button(self.save_button)
            self.ok_label.setText("Success")
            self.ok_label.setStyleSheet("color:green")
        else:
            output_result = "'%s'" % result
            self.disable_button(self.save_button)
            self.ok_label.setText("Failed")
            self.ok_label.setStyleSheet("color:red")

        self.test_connection_button.setText(self.text_test_connection_button)
        self.enable_button(self.test_connection_button)
