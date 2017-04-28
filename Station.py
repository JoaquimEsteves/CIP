# !/usr/bin/python
# -*- coding: utf-8 -*-
import settings
import protocols
from utils import Logger
log = Logger(debug=settings.DEBUG)
class Station(object):
    def __init__(self, connection, name):
        self._connection = connection
        self._name = name
        self._messages = settings.getMessagesForStation(name)
        self._stage = -1
		
	def handle(connection):
		return None
