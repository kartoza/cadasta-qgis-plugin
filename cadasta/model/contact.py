# coding=utf-8
"""
Cadasta project - **Contact Model.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '28/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

from qgis.PyQt.QtSql import QSqlQuery
from cadasta.database.cadasta_database import CadastaDatabase

_table = 'contact'


class Contact():
    """Contact model."""
    id = None
    firstname = None
    lastname = None
    email = None
    phone = None
    _fields = ['id', 'firstname', 'lastname', 'email', 'phone']

    def __init__(self, id=None,
                 firstname=None, lastname=None, email=None, phone=None):
        """Constructor.
        """
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        CadastaDatabase.open_database()
        self._create_database()

    def _create_database(self):
        """Create table function."""
        query_fields = ('id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'firstname varchar(20) NOT NULL,'
                        'lastname varchar(20),'
                        'email varchar(20),'
                        'phone varchar(20)')
        query_string = 'create table %(TABLE)s (%(query_field)s)' % \
                       {
                           'TABLE': _table,
                           'query_field': query_fields
                       }
        query = QSqlQuery()
        query.exec_(query_string)

    def save(self):
        """Save this object to database

        :return: id of row that is inserted
        :rtype: int
        """

        data = {}
        if self.id:
            data['id'] = self.id
        if self.firstname:
            data['firstname'] = u'\"%s\"' % self.firstname
        if self.lastname:
            data['lastname'] = u'\"%s\"' % self.lastname
        if self.email:
            data['email'] = u'\"%s\"' % self.email
        if self.phone:
            data['phone'] = u'\"%s\"' % self.phone

        # save to database
        row_id = CadastaDatabase.save_to_database(_table, data)
        if row_id >= 1:
            self.id = row_id
        return self.id

    def delete(self):
        """Delete this object
        """
        CadastaDatabase.delete_rows_from_database(_table, [self.id])
        del self

    @staticmethod
    def get_rows(**kwargs):
        """Get filtered rows from kwargs

        :return: List of json of the rows
        :rtype: [dict]
        """
        query_filter = []
        filter_string = '%(FIELD)s=%(VALUE)s'
        for key, value in kwargs.iteritems():
            if key != 'id':
                value = '"%s"' % value

            # append it to query filter
            query_filter.append(filter_string % {
                'FIELD': key,
                'VALUE': value
            })
        query = CadastaDatabase.get_from_database(
            _table, ','.join(query_filter))

        #  convert
        output = []
        while (query.next()):
            output.append(
                Contact(
                    id=query.value(0),
                    firstname=query.value(1),
                    lastname=query.value(2),
                    email=query.value(3),
                    phone=query.value(4)
                )
            )
        return output
