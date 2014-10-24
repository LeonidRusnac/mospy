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

	def getTrainLevels(self):
		#/petarena/train/2087233/
		response = self.session.get(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/')
		if response.url == (self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/'):
			tree = html.fromstring(response.text)
			return tree.xpath('//span[@class="num"]/text()')
		else:
			print 'Error getTrainLevel, be sure not blocked somewhere!'

	def train(self, skill):
		if skill not in ['focus', 'loyality', 'mass']:
			print "Error skill type!"
		else:
			response = self.session.post(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/'+skill+'/', data={
				'action': 'train',
				'pet': self.petid,
				'skill': skill
			})

			print "done training!"

	def getTrainTimer(self):
		response = self.session.get(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/')
		if response.url == (self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/'):
			tree = html.fromstring(response.text)
			tim =tree.xpath('//span[@id="train"]/@timer')
			if not tim:
				tim = 0
			else:
				tim = tim[0]
			return tim
		else:
			print 'Error getTrainLevel, be sure not blocked somewhere!'

	def getDescription(self):
		response = self.session.get(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/')
		if response.url == (self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/'):
			tree = html.fromstring(response.text)
			pethp = tree.xpath('//span[@id="pethp"]/text()')[0].split('/')
			tonus = tree.xpath('//div[@id="pet-tonus"]/span[@rel="tonus"]/text()')[0]
			t = self.getTrainLevels()
			return {'hp': pethp[0], 'maxhp': pethp[1], 'tonus': tonus, 'timer': self.getTrainTimer(), 'focus': t[0], 'loyality': t[1], 'mass': t[2]}
		else:
			print 'Error getTrainLevel, be sure not blocked somewhere!'

	def cuddle(self):
		#post("/petarena/mood/" + pet + "/", {"action": "mood", "pet": pet, "ajax": 1, "postkey": postVerifyKey},
		response = self.session.post(self.config['siteUrl']+'petarena/mood/'+str(self.petid)+'/', data={
			'action': 'mood',
			'pet': self.petid
		})

		print "done cuddling!"
