# coding=utf-8
"""
Cadasta **Cadasta Database.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.


"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '27/12/16'

import logging
from qgis.PyQt import QtSql
from cadasta.common.setting import get_path_database

LOGGER = logging.getLogger('CadastaQGISPlugin')

database = 'QSQLITE'
database_name = get_path_database('cadasta.db')


class CadastaDatabase(object):
    """Cadasta class to handle databasel."""

    def __init__(self):
        """Constructor for the class."""

    @staticmethod
    def open_database():
        """open Database
        """
        db = QtSql.QSqlDatabase.addDatabase(database)
        if db:
            db.setDatabaseName(database_name)
            if not db.open():
                LOGGER.debug("not opened")

    @staticmethod
    def save_to_database(table, data):
        """save Into database.

        :param table: table target be inserted
        :type table: str

        :param data: data to be inserted
        :type data: dict

        :return: id of row that is inserted
        :rtype: int
        """
        CadastaDatabase.open_database()
        if 'id' in data:
            # updating existing data
            row_id = data['id']
            del data['id']

            query_filter = []
            filter_string = '%(FIELD)s=%(VALUE)s'
            for key, value in data.iteritems():
                value = value
                # append it to query filter
                query_filter.append(filter_string % {
                    'FIELD': key,
                    'VALUE': value
                })
            query_string = (
                               'UPDATE %(TABLE)s SET %(SET)s '
                               'WHERE id=%(ID)s'
                           ) % {
                               'TABLE': table,
                               'SET': ','.join(query_filter),
                               'ID': row_id
                           }
        else:
            # inserting new data
            fields = []
            values = []
            for key, value in data.iteritems():
                fields.append(key)
                values.append(value)
            query_string = (
                               'INSERT INTO %(TABLE)s (%(FIELDS)s) '
                               'VALUES (%(VALUES)s)'
                           ) % {
                               'TABLE': table,
                               'FIELDS': ','.join(fields),
                               'VALUES': ','.join(values)
                           }
        query = QtSql.QSqlQuery()
        query.exec_(query_string)
        if query.numRowsAffected() < 1:
            return -1
        else:
            return query.lastInsertId()

    @staticmethod
    def get_from_database(table, filter_string):
        """get rows from database.

        :param table: table target be inserted
        :type table: str

        :param filter_string: filter_string that will be used as filter
        :type filter_string: str

        :return: Query that is received
        :rtype: QSqlQuery
        """
        CadastaDatabase.open_database()
        query_string = (
            'SELECT * FROM %(TABLE)s ' % {'TABLE': table}
        )
        if filter_string:
            query_string += 'WHERE %s' % filter_string
        query = QtSql.QSqlQuery()
        query.exec_(query_string)
        return query

    @staticmethod
    def delete_rows_from_database(table, row_ids):
        """delete rows from database.

        :param table: table target be inserted
        :type table: str

        :param row_ids: list id of row that will be deleted
        :type row_ids: [int]
        """
        CadastaDatabase.open_database()
        row_ids = ['%s' % row_id for row_id in row_ids]
        query_string = (
            'DELETE FROM %(TABLE)s WHERE ID IN (%(ID)s)' % {
                'TABLE': table, 'ID': ','.join(row_ids)
            }
        )
        query = QtSql.QSqlQuery()
        query.exec_(query_string)
