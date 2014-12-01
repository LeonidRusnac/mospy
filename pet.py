#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class FightingPet(object):
	def __init__(self, session, userConfig, petid):
		self.petid = petid
		self.session = session
		self.config = userConfig

	def getTrainLevels(self):
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
			self.session.post(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/'+skill+'/', data={
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
			print 'Error getDescription, be sure not blocked somewhere!'

	def cuddle(self):
		self.session.post(self.config['siteUrl']+'petarena/mood/'+str(self.petid)+'/', data={
			'action': 'mood',
			'pet': self.petid
		})

		print "done cuddling!"

	def setActive(self):
		self.session.post(self.config['siteUrl']+'petarena/active/'+str(self.petid)+'/', data={
			'action': 'active',
			'pet': self.petid,
			'type': 'battle'
		})

		print "done set active!"


class JoggingPet(object):
	def __init__(self, session, userConfig, petid):
		self.petid = petid
		self.session = session
		self.config = userConfig
		
	def getTrainLevels(self):
		response = self.session.get(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/arena/')
		if response.url == (self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/arena/'):
			tree = html.fromstring(response.text)
			return tree.xpath('//span[@class="num"]/text()')
		else:
			print 'Error getTrainLevel, be sure not blocked somewhere!'

	def train(self, skill):
		if skill not in ['acceleration', 'speed', 'endurance', 'dexterity']:
			print "Error skill type!"
		else:
			self.session.post(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/'+skill+'/', data={
				'action': 'train',
				'pet': self.petid,
				'skill': skill
			})

			print "done training!"

	def getDescription(self):
		response = self.session.get(self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/arena/')
		if response.url == (self.config['siteUrl']+'petarena/train/'+str(self.petid)+'/arena/'):
			tree = html.fromstring(response.text)
			
			pethp = tree.xpath('//li[@class="progressbar tonus"]/span/div/span/text()')[0]
			t = self.getTrainLevels()

			return {'hp': pethp, 'acceleration': t[0], 'speed': t[1], 'endurance': t[2], 'dexterity': t[3]}
		else:
			print 'Error getDescription, be sure not blocked somewhere!'


	def registerRace(self):
		#/petrun/signup/race/
		self.session.post(self.config['siteUrl']+'petrun/signup/race/', data={
				'__ajax': 1,
				'return_url': '/petrun/',
				'pet-names': self.petid,
				'tickets-type': 'free_ticket'
			})


