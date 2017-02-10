# coding=utf-8
"""
Cadasta Contact -**Cadasta Widget**

This module provides: Login : Login for cadasta and save authnetication

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
import re

from qgis.gui import QgsMessageBar
from PyQt4.QtGui import (
    QHeaderView,
    QAbstractItemView
)
from cadasta.gui.tools.wizard.wizard_step import WizardStep
from cadasta.gui.tools.wizard.wizard_step import get_wizard_step_ui_class
from cadasta.model.party import Party

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

FORM_CLASS = get_wizard_step_ui_class(__file__)

LOGGER = logging.getLogger('CadastaQGISPlugin')


class StepProjectUpdate04(WizardStep, FORM_CLASS):
    """Contact widget."""

    def __init__(self, parent=None):
        """Constructor.

        :param parent: parent - widget to use as parent.
        :type parent: QWidget
        """
        super(StepProjectUpdate04, self).__init__(parent)
        # Create model
        self.project = None
        self.model = None

    def get_next_step(self):
        """Find the proper step when user clicks the Next button.

        :returns: The step to be switched to
        :rtype: WizardStep, None
        """
        return None

    def set_widgets(self):
        """Set all widgets."""
        self.project = self.parent.project['information']
        organization_slug = self.project['organization']['slug']
        project_slug = self.project['slug']
        filters = list()
        filters.append("project_slug ='" + project_slug + "'")
        filters.append("organization_slug ='" + organization_slug + "'")
        self.model = Party.table_model(filters)

        self.contact_listview.horizontalHeader().setStretchLastSection(True)
        self.contact_listview.horizontalHeader().setResizeMode(
            QHeaderView.Stretch)
        self.contact_listview.setModel(self.model)
        self.contact_listview.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.add_button.clicked.connect(self.add_party)
        self.save_button.clicked.connect(self.save_model)

        self.contact_listview.hideColumn(0)
        self.contact_listview.hideColumn(1)
        self.contact_listview.hideColumn(4)
        self.contact_listview.hideColumn(5)
        self.contact_listview.hideColumn(6)

    def add_party(self):
        """Add party."""
        row = self.model.rowCount()
        self.model.insertRows(row, 1)

    def validate_email(self, email):
        """Delete email.

        :param email: email that will be checked.
        :type email: str

        :return: boolean is validated or not
        :rtype: bool
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def save_model(self):
        """Save model contact."""
        error = None
        for i in xrange(self.model.rowCount()):
            record = self.model.record(i)
            if record.value("id") or record.value("name"):
                is_deleted = True
            else:
                is_deleted = False
            if is_deleted:
                if not record.value("email") and not record.value("phone"):
                    error = self.tr(
                        'One or more contact doesn\'t has email and '
                        'phone. Either email or phone must be provided.')
                    break
                    # validate email
                if record.value("email") and not self.validate_email(
                        record.value("email")):
                    error = self.tr(
                        'There is one or more wrong email in contact ist.')

        if not error:
            self.model.submitAll()
        else:
            self.message_bar = QgsMessageBar()
            self.message_bar.pushWarning(
                self.tr('Error'),
                error
            )
