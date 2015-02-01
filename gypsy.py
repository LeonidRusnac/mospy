#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Gypsy(object):
	def __init__(self, session, userConfig):
		self.session = session
		self.config = userConfig

	def gypsyPlay(self):
		response = self.session.get(self.config['siteUrl']+'camp/gypsy/')
		if response.url == (self.config['siteUrl']+'camp/gypsy/'):
			self.session.post(self.config['siteUrl']+'camp/gypsy/', data={
				'action': 'gypsyStart',
				'gametype': 0
			})

			print "Gypsy start!"

			self.session.post(self.config['siteUrl']+'camp/gypsy/', data={
				'action': 'gypsyAuto'
			})

			print "Gypsy done!"



		else:
			print 'Error play with gypsy, be sure not blocked somewhere!'
