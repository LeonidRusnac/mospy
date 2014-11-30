#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html
from random import shuffle

class Metro(object):
	'''Class that do the work in metro'''
	def __init__(self, session, userConfig):
		self.session = session
		self.config = userConfig

	def attackRat(self):
		'''get timer of new start'''
		'''get level, and time to wait''' #dashedlink
		response = self.session.get(self.config['siteUrl']+'metro/')
		if response.url == (self.config['siteUrl']+'metro/'):

			tree = html.fromstring(response.text)
			
			if not tree.xpath('//small[@class="dashedlink"]/@timer'):
				#response = self.session.post(self.config['siteUrl']+'factory/start-petriks/', data={
				#	'player' : self.config['playerId']
				#})

				print 'liv 1'
			else:
				print 'not init'
		else:
			print 'Error attacking rat, be sure not blocked somewhere!'

	def claimBonus(self):
		'''If possible claim the bonus'''
		pass

	def playThimble(self, sum, nine=True):
		# trasform money to ruda
		self.session.get(self.config['siteUrl']+'thimble/start/')

		for i in range(0, sum/1500):
			x = range(0, 9)
			shuffle(x)
			self.session.get(self.config['siteUrl']+'thimble/play/9/0/')
			self.session.get(self.config['siteUrl']+'thimble/guess/'+str(x[0])+'/')
			self.session.get(self.config['siteUrl']+'thimble/guess/'+str(x[1])+'/')
			self.session.get(self.config['siteUrl']+'thimble/guess/'+str(x[2])+'/')

		self.session.get(self.config['siteUrl']+'thimble/leave/')



		pass

	def metrowarRegister(self):
		pass

	def metroBranch(self):
		pass

	def getRobotData(self):
		pass

	def claimRobotResources(self):
		pass



