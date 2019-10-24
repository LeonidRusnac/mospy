#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Factory(object):
	"""do the factory functions"""
	def __init__(self, session, userConfig):
		self.session = session
		self.config = userConfig

	def makePetriks(self):
		response = self.session.get(self.config['siteUrl']+'factory/')
		if response.url == (self.config['siteUrl']+'factory/'):

			tree = html.fromstring(response.text)
			timerPet = tree.xpath('//span[@id="petriksprocess"]/@timer')

			if not timerPet:
				response = self.session.post(self.config['siteUrl']+'factory/start-petriks/', data={
					'player' : self.config['playerId']
				})

				return True
			
		return False	
