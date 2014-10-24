#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Pet(object):
	def __init__(self, session, userConfig, petid):
		self.petid = petid
		self.session = session
		self.config = userConfig

	def getTrainLevel(self):
		#/petarena/train/2087233/
		response = self.session.get(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/')
		if response.url == (self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/'):
			tree = html.fromstring(response.text)
			print tree.xpath('//span[@class="num"]/text()')
		else:
			print 'Error getTrainLevel, be sure not blocked somewhere!'