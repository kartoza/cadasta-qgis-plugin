# coding=utf-8
"""
Cadasta project - **Base Model.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '28/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

from cadasta.database.cadasta_database import CadastaDatabase


class BaseModel():
    """Contact model."""

    def __init__(self):
        """Constructor.
        """
        super(BaseModel, self).__init__()

    @staticmethod
    def insert_row(fields, table, database_name, **kwargs):
        """Inser row with data from kwargs

        :param fields: Dict of field to be inserted
        :type fields: dict

        :param table: table target be inserted
        :type table: str

        :param database_name: database name that will be used
        :type database_name: str

        :return: id of row that is inserted
        :rtype: int
        """
        data_value = {}
        for key in kwargs:
            if key in fields:
                data_value[key] = kwargs[key]

        inserted_fields = []
        inserted_values = []
        for key, value in kwargs.iteritems():
            if key in fields:
                inserted_fields.append(key)
                if fields[key] == str:
                    inserted_values.append(u'\"%s\"' % value)
                else:
                    inserted_values.append(value)
        return CadastaDatabase.insert_to_database(
            table, inserted_fields, inserted_values, database=database_name)
