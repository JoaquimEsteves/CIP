# !/usr/bin/python
# -*- coding: utf-8 -*-
"""All project settings are defined here"""
import os
# Set loggin as debug level
DEBUG = True

# Translation Contact Server default configuration
DEFAULT_NAME = 'localhost'
DEFAULT_PORT = 58000

# Size for buffer to hold all messages send between client and server (1024bytes*4*1024 = 4mb)
BUFFERSIZE = 4096 * 1024

# Timeout delay that we accept between connections, in seconds
TIMEOUT_DELAY = 5

# Misc properties

acceptable_IDs = ["QC","StorageAndAssembly","Scorbot","AGV","Belt", "RFID"]

def getMessagesForStation(name):
	if name == "QC":
		return ["[SUP]Check Stage1", "[SUP] Check Stage2"]
	elif name == "StorageAndAssembly":
		return ["[SUP]Start Stage1", "[SUP] Start Stage2"]
	elif name == "Scorbot":
		return ["[SUP]Take Piece out of belt"]
	elif name == "AGV":
		return ["[SUP]Resuply Storage"]
	elif name == "Belt":
		return ["[SUP]GOTO QC","[SUP]GOTO STORAGE", "[SUP]GOTO SCORBOT", "[SUP]GOTO TRASH"]
	elif name == "RFID":
		return ["[SUP]PLEASE GIVE US THE ID"]
