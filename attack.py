#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Attack(object):
	'''A class that contains methods for attacks'''

	def __init__(self, session, userConfig):
		self.session = session
		self.config = userConfig

	def attack(self, typeA='', min=0, max=0, id=0):
		'''
		if id attack by id, if not type attack by levels 
		else attack by type
		'''
		if id != 0:
			print 'Attack by id'
		elif typeA == '':
			print 'Attack by levels'
		else:
			print 'Attack by type'