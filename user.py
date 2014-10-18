#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

class User(object):
	'''Rappresents a user profile'''
	def __init__(self, session, userConfig):
		self.session = session
		self.config = userConfig #dictionary with siteUrl, login, password, cookies_file

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
			print "Already logged in"

	def logout(self):
		'''Log out if logged in'''
		self.session = None
		if os.path.exists(self.cm['cookies_file']):
			os.remove(self.cm['cookies_file'])

	def getInfo(self):
		'''Return the info data of a user'''
		pass

	def getTimers(self):
		'''Return the timers'''
		pass

'''
#userConfig example
userConfig = dict{
	'siteUrl' : 'http://bbb.xx/',
	'login' : 'aaa@cc.xx',
	'password' : '123456',
	'cookies_file' : 'path/to/file'
}
'''
