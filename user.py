#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import pickle # simle write/read data from files
import requests
from lxml import html
import sys, os

class User(object):
	'''Rappresents a user profile'''
	def __init__(self, session, userConfig):
		self.session = session
		self.config = userConfig #dictionary with siteUrl, login, password, cookies_file

		if os.path.exists(self.config['cookies_file']):
			try:
				with open(self.config['cookies_file']) as f:
					self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
			except IOError:
				pass
				#print "The cookies file doesn't exists"

	def logged(self):
		'''Check if the user is logged in'''
		response = self.session.get(self.config['siteUrl'] + "player/")

		#if I was redirected to the main page I'm not logged in
		if response.url == self.config['siteUrl']:
			return False
		return True


	def login(self):
		'''Log in if not logged'''
		if not self.logged():
			response = self.session.post(self.config['siteUrl'], data={
				'action' : 'login',
				'email' : self.config['login'],
				'password' : self.config['password'],
				'remember' : '1'
			})

			page = response.text
			if 'main010.png' in page:
				sys.stderr.write("Wrong pair username/password, aborting.")
				sys.exit(1)
			else:
				with open(self.config['cookies_file'], 'w') as f:
					pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
				print "Congrats, you're now logged in"
		else:
			# print "Already logged in"
            pass

	def logout(self):
		'''Log out if logged in'''
		self.session = requests.Session()
		if os.path.exists(self.config['cookies_file']):
			os.remove(self.config['cookies_file'])

	def getInfo(self):
		'''Return the info data of a user'''
		info = {}
		if self.logged():
			response = self.session.get(self.config['siteUrl'] + 'player/')

			if response.url == (self.config['siteUrl']+'player/'):
				tree = html.fromstring(response.text)
				info['current_hp'] = tree.xpath('//span[@id="currenthp"]/text()')[0]
				info['max_hp'] = tree.xpath('//span[@id="maxhp"]/text()')[0]
				info["current_tonus"] = tree.xpath('//span[@id="currenttonus"]/text()')[0]
				info["max_tonus"] = tree.xpath('//span[@id="maxenergy"]/text()')[0]

				info["money"] = tree.xpath('//span[@rel="money"]/text()')[0]
				info["ore"] = tree.xpath('//span[@rel="ore"]/text()')[0]
				info["oil"] = tree.xpath('//span[@rel="oil"]/text()')[0]
				info["honey"] = tree.xpath('//span[@rel="honey"]/text()')[0]
			else:
				print 'Error into grab user info'
		else:
			print 'Please log in first'
		return info

	def getTimers(self):
		'''Return the timers'''
		if self.logged():
			response = self.session.get(self.config['siteUrl'] + 'player/')

			if response.url == (self.config['siteUrl']+'player/'):
				tree = html.fromstring(response.text)
				return tree.xpath('//a[@id="timeout"]/@timer')[0] , tree.xpath('//a[@id="timeout2"]/@timer')[0]
			else:
				print 'Error into grab user timers'
		else:
			print 'Please log in first'
		return '', ''

'''
#userConfig example
userConfig = {
	'siteUrl' : 'http://bbb.xx/',
	'login' : 'aaa@cc.xx',
	'password' : '123456',
	'cookies_file' : 'path/to/file'
}
'''
