# coding=utf-8

"""Tests for organization project api.
"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/12/16'

import unittest

import os
from qgis.PyQt.QtCore import QCoreApplication
from cadasta.api.organization_project import OrganizationProject, OrganizationProjectSpatial

if not os.environ.get('ON_TRAVIS', False):
    from cadasta.test.utilities import get_qgis_app

    QGIS_APP = get_qgis_app()


class OrganizationProjectTest(unittest.TestCase):
    """Test project api works."""

    def setUp(self):
        """Runs before each test."""
        self.organization_slug = 'any-given-sunday'
        self.project_slug = 'san-jose-open-data-portal-affordable-housing'

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_organization_project(self):
        """Test organization project api."""
        organization_project = OrganizationProject(self.organization_slug)
        # Wait until it finished
        while not organization_project.reply.isFinished():
            QCoreApplication.processEvents()
        self.assertIsNotNone(organization_project.get_json_results())

    def test_organization_project_spatial(self):
        """Test organization project api spatial."""
        organization_project = OrganizationProjectSpatial(self.organization_slug, self.project_slug)
        # Wait until it finished
        while not organization_project.reply.isFinished():
            QCoreApplication.processEvents()
        self.assertIsNotNone(organization_project.get_json_results())


if __name__ == "__main__":
    suite = unittest.makeSuite(OrganizationProjectTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
