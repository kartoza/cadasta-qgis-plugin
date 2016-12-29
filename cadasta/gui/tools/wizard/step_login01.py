# coding=utf-8
"""
Cadasta Login step -**Cadasta Wizard**

This module provides: Project Creation Step 1 : Define basic project properties

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from qgis.gui import QgsMessageBar
from cadasta.api.login import Login
from cadasta.common.setting import save_authtoken, save_url_instance
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepLogin1(WizardStep, FORM_CLASS):
    """Step 1 for Login"""

    def __init__(self, parent=None):
        """Constructor

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepLogin1, self).__init__(parent)

    def set_widgets(self):
        """Set all widgets on the tab."""
        self.text_test_connection_button = self.test_connection_button.text()
        self.ok_label.setVisible(False)
        self.save_button.setEnabled(False)

        self.test_connection_button.clicked.connect(
            self.login
        )
        self.save_button.clicked.connect(
            self.save_authtoken
        )

    def validate_step(self):
        """Check if the step is valid.

        :returns: Tuple of validation status and error message if any
        :rtype: ( bool, str )
        """
        return True, ''

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

           This method must be implemented in derived classes.

        :returns: The step to be switched to
        :rtype: WizardStep instance or None
        """
        return None

    def login(self):
        """Login function when tools button clicked."""

        username = self.username_input.displayText()
        password = self.password_input.text()
        self.url = self.url_input.displayText()
        self.auth_token = None

        self.save_button.setEnabled(False)
        self.ok_label.setVisible(False)

        if not self.url or not username or not password:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                self.tr('Error'),
                self.tr('URL/Username/password is empty.')
            )
        else:
            self.test_connection_button.setEnabled(False)
            self.test_connection_button.setText(self.tr('Logging in...'))
            # call tools API
            self.login_api = Login(
                self.url,
                username,
                password,
                self.on_finished)

    def on_finished(self, result):
        """On finished function when tools request is finished."""

        self.ok_label.setVisible(True)
        if 'auth_token' in result:
            self.auth_token = result['auth_token']
            self.save_button.setEnabled(True)
            self.ok_label.setText(self.tr('Success'))
            self.ok_label.setStyleSheet('color:green')
        else:
            self.save_button.setEnabled(False)
            self.ok_label.setText(self.tr('Failed'))
            self.ok_label.setStyleSheet('color:red')

        self.test_connection_button.setText(self.text_test_connection_button)
        self.test_connection_button.setEnabled(True)

    def save_authtoken(self):
        """Save received authtoken to setting."""

        if self.auth_token:
            save_authtoken(self.auth_token)
            save_url_instance(self.url)
            self.parent.close()