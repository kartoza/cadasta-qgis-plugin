# coding=utf-8
"""
InaSAFE Disaster risk assessment tool developed by AusAid -
  **Logging related code.**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import os
import sys
import logging

from qgis.core import QgsMessageLog
# pylint: enable=F0401
from cadasta.utilities.i18n import tr

# This is ugly but we dont have a better solution yet...
safe_extras_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'safe_extras'))
if safe_extras_dir not in sys.path:
    sys.path.append(safe_extras_dir)

__author__ = 'tim@kartoza.com'
__revision__ = '$Format:%H$'
__date__ = '29/01/2011'
__copyright__ = 'Copyright 2016, Cadasta'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class QgsLogHandler(logging.Handler):
    """A logging handler that will log messages to the QGIS logging console."""

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        """Try to log the message to QGIS if available, otherwise do nothing.

        :param record: logging record containing whatever info needs to be
                logged.
        """
        try:
            # Check logging.LogRecord properties for lots of other goodies
            # like line number etc. you can get from the log message.
            QgsMessageLog.logMessage(
                record.getMessage(),
                'CadastaQGISPlugin',
                0
            )
        except MemoryError:
            message = tr(
                'Due to memory limitations on this machine, Cadasta can not '
                'handle the full log')
            print message
            QgsMessageLog.logMessage(message, 'CadastaQGISPlugin', 0)


def add_logging_handler_once(logger, handler):
    """A helper to add a handler to a logger, ensuring there are no duplicates.

    :param logger: Logger that should have a handler added.
    :type logger: logging.logger

    :param handler: Handler instance to be added. It will not be added if an
        instance of that Handler subclass already exists.
    :type handler: logging.Handler

    :returns: True if the logging handler was added, otherwise False.
    :rtype: bool
    """
    class_name = handler.__class__.__name__
    for logger_handler in logger.handlers:
        if logger_handler.__class__.__name__ == class_name:
            return False

    logger.addHandler(handler)
    return True


def setup_logger(logger_name):
    """Run once when the module is loaded and enable logging.

    Borrowed heavily from this:
    http://docs.python.org/howto/logging-cookbook.html

    Now to log a message do::

       LOGGER.debug('Some debug message')

    .. note:: The file logs are written to the CadastaQGISPlugin
        user tmp dir e.g.:
       /tmp/CadastaQGISPlugin/23-08-2012/timlinux/logs/CadastaQGISPlugin.log

    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create formatter that will be added to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # create a QGIS handler
    qgis_handler = QgsLogHandler()

    # Set formatters
    console_handler.setFormatter(formatter)
    qgis_handler.setFormatter(formatter)

    # add the handlers to the logger
    add_logging_handler_once(logger, console_handler)
    add_logging_handler_once(logger, qgis_handler)
