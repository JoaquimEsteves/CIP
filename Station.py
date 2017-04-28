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

class QCStation(Station):
	def __init__(self,host,port,name="QC"):
		super.(QCStation,self).__init__(host,port,name)
		
	def handle(self,connection):
		if self.stage == -1:
            #Nothing todo
		
		elif self.stage == 0:
			res = self._TCP.request(connection,self._messages[0])
			if res[:-2] == "OK":
				self._stage = 1
				self._TCP.request(connection,"Good Job Friend!")
			elif res[:-2] == "NOK":
				self._state = 0
				self._TCP.request(connection,"You have failed me!")
		elif self.stage == 1:
			res = self._TCP.request(connection,self._messages[1])
			if res[:-2] == "OK":
				self._stage = 2
				self._TCP.request(connection,"Good Job Friend!")
			elif res[:-2] == "NOK":
				self._state = 0
				self._TCP.request(connection,"You have failed me!")
		else:
			log.error("[QCSTATION] I am in a state I shouldn't be in! {}".format(self._stage))
			
class StorAndAssemblStation(Station):
	def __init__(self,host,port,name="QC"):
		super.(QCStation,self).__init__(host,port,name)
		
	def handle(self,connection):
		if self.stage == 0:
			res = self._TCP.request(connection,self._messages[0])
			if res[:-2] == "OK":
				self._stage = 1
				self._TCP.request(connection,"Good Job Friend!")
			elif res[:-2] == "NOK":
				self._state = 0
				self._TCP.request(connection,"You have failed me!")
		if self.stage == 1:
			res = self._TCP.request(connection,self._messages[1])
			if res[:-2] == "OK":
				self._stage = 2
				self._TCP.request(connection,"Good Job Friend!")
			elif res[:-2] == "NOK":
				self._state = 0
				self._TCP.request(connection,"You have failed me!")
		else:
			log.error("[StorAndAssemblSTATION] I am in a state I shouldn't be in! {}".format(self._stage))
			
class QCStation(Station):
	def __init__(self,host,port,name="QC"):
		super.(QCStation,self).__init__(host,port,name)
		
	def handle(self,connection):
		if self.stage == 0:
			res = self._TCP.request(connection,self._messages[0])
			if res[:-2] == "OK":
				self._stage = 1
				self._TCP.request(connection,"Good Job Friend!")
			elif res[:-2] == "NOK":
				self._state = 0
				self._TCP.request(connection,"You have failed me!")
		if self.stage == 1:
			res = self._TCP.request(connection,self._messages[1])
			if res[:-2] == "OK":
				self._stage = 2
				self._TCP.request(connection,"Good Job Friend!")
			elif res[:-2] == "NOK":
				self._state = 0
				self._TCP.request(connection,"You have failed me!")
		else:
			log.error("[QCSTATION] I am in a state I shouldn't be in! {}".format(self._stage))			
	
class TRSHandler(object):
	"""Class to wrap all Endpoints for TRS messages."""
	def __init__(self, language, host=settings.DEFAULT_TRS_NAME, port=settings.DEFAULT_TRS_PORT):
		"""inits udp instance (TRS SERVER)"""
		self.TCP = protocols.TCP(host, port)
		self.language = language

	def dispatch(self, data):
		"""this method parses and checks for with feature is the "data" requesting
		this works as a central hub, "switch", where it redirects to the correct
		method. as input is the data from the outside world, output is the
		handled data"""
		# removes \n from string
		data = self.TCP._remove_new_line(data)
		# split data into chunks
		data = data.split(" ")
		# get protocol and rest of the data
		protocol = data[0]
		data = data[1:]
		# dispatch to correct method
		if protocol == "TRQ":
			data = self._TRQ(data)
		else:
			data = "ERR"
		# put back the \n
		data += "\n"
		return data
