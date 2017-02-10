# coding=utf-8
"""
Cadasta project - **Relationship Model.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from PyQt4.QtSql import QSqlQuery
from cadasta.database.cadasta_database import CadastaDatabase

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '28/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class Party(object):
    """Party model."""

    id = None
    party_id = None
    name = None
    type = None
    attributes = None
    project_slug = None
    organization_slug = None
    _fields = ['id', 'party_id', 'name', 'type', 'project_slug', 'organization_slug', 'attributes']
    displayed_fields = ['name', 'type']

    def __init__(self,
                 id=None,
                 party_id=None,
                 name=None,
                 type=None,
                 project_slug=None,
                 organization_slug=None,
                 attributes=None, ):
        """Constructor.

        :param id: id of contact.
        :type id: int

        :param name: name of contact.
        :type name: str

        :param email: email of contact.
        :type email: str

        :param phone: phone of contact.
        :type phone: str
        """
        self.id = id
        self.party_id = party_id
        self.name = name
        self.type = type
        self.project_slug = project_slug
        self.organization_slug = organization_slug
        self.attributes = attributes
        Party.create_database()

    def save(self):
        """Save this object to database.

        :return: id of row that is inserted
        :rtype: int
        """

        data = {}
        if self.id:
            data['id'] = self.id
        if self.party_id:
            data['party_id'] = u'\"%s\"' % self.party_id
        if self.name:
            data['name'] = u'\"%s\"' % self.name
        if self.type:
            data['type'] = u'\"%s\"' % self.type
        if self.attributes:
            data['attributes'] = u'\"%s\"' % self.attributes
        if self.project_slug:
            data['project_slug'] = u'\"%s\"' % self.project_slug
        if self.organization_slug:
            data['organization_slug'] = u'\"%s\"' % self.organization_slug

        # save to database
        row_id = CadastaDatabase.save_to_database(
            Party.__name__, data)
        if row_id >= 1:
            self.id = row_id
        return self.id

    def delete(self):
        """Delete this object
        """
        CadastaDatabase.delete_rows_from_database(
            Party.__name__, [self.id])
        del self

    def get_row_by_party_id(self, party_id):
        """Get row by party id
        """
        query = CadastaDatabase.get_from_database(
                Party.__name__, 'WHERE party_id=%s' % party_id)
        query.first()
        query.previous()
        while query.next():
            return Party(
                    id=query.value(0),
                    party_id=query.value(1),
                    name=query.value(2),
                    type=query.value(3),
                    project_slug=query.value(4),
                    organization_slug=query.value(5),
                    attributes=query.value(6))

    # ------------------------------------------------------------------------
    # STATIC METHOD
    # ------------------------------------------------------------------------
    @staticmethod
    def create_database():
        """Create table function."""
        db = CadastaDatabase.open_database()
        query_fields = ('id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'party_id varchar(100) NOT NULL UNIQUE,'
                        'name varchar(100) NOT NULL,'
                        'type varchar(20),'
                        'project_slug varchar(100) NOT NULL,'
                        'organization_slug varchar(100) NOT NULL,'
                        'attributes varchar(150)')
        query_string = 'create table %(TABLE)s (%(query_field)s)' % \
                       {
                           'TABLE': Party.__name__,
                           'query_field': query_fields
                       }
        query = QSqlQuery()
        query.exec_(query_string)

        if db:
            db.close()

    @staticmethod
    def get_rows(**kwargs):
        """Get filtered rows from kwargs.

        :return: List of Party
        :rtype: [Party]
        """
        query_filter = []

        filter_string = '%(FIELD)s=%(VALUE)s'
        for key, value in kwargs.iteritems():
            if key in Party.displayed_fields:
                value = '"%s"' % value

            # append it to query filter
            query_filter.append(filter_string % {
                'FIELD': key,
                'VALUE': value
            })

        LOGGER.debug(','.join(query_filter))
        query = CadastaDatabase.get_from_database(
            Party.__name__, ','.join(query_filter))

        #  convert
        output = []
        query.first()
        query.previous()
        while query.next():
            output.append(
                Party(
                    id=query.value(0),
                    party_id=query.value(1),
                    name=query.value(2),
                    type=query.value(3),
                    project_slug=query.value(4),
                    organization_slug=query.value(5),
                    attributes=query.value(6)
                )
            )
        return output

    @staticmethod
    def table_model(filters=None):
        """Get Table Model for Party.

        :return: Table Model for contact
        :rtype: QSqlTableModel
        """
        Party.create_database()
        return CadastaDatabase.get_table_model(Party.__name__, filters)
