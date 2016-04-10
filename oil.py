#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__ = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__ = "0.1"

from lxml import html
import re


class Oil(object):

    def __init__(self, session, userConfig):
        self.session = session
        self.config = userConfig

    def getProgress(self):
        if self.isOldOil():
            progress = -1
        else:
            response = self.session.get(self.config['siteUrl'] + "neftlenin/")

            tree = html.fromstring(response.text)
            progress = tree.xpath(
                '//div[@class="progress-wrapper"]//i[@class="counter"]/text()')[0]
        return progress

    def getCurrentLevelNumber(self):
        if self.isOldOil():
            response = self.session.get(self.config['siteUrl'] + "neft/")
            tree = html.fromstring(response.text)
            number = len(tree.xpath('//i[contains(@class, "icon-locked pulp")]'))
            return 16 - number
        else:
	    response = self.session.post(self.config['siteUrl'] + 'neftlenin/', data={
		'action': 'getPrize'
	    })

	    #print response.text.encode('ascii', 'ignore')

	    page = response.text.encode('ascii', 'ignore')
	    match = re.findall('\"step\":\"[0-9]*\"', page)
	    if len(match) == 1:
		    lvl = re.findall('[0-9]+', match[0])
		    if len(lvl) == 1:
			return int(lvl[0])


    def getCurrentLevelType(self):
        if self.isOldOil():
            return 'd'
        else:
	    response = self.session.post(self.config['siteUrl'] + 'neftlenin/', data={
		'action': 'getPrize'
	    })

	    page = response.text.encode('ascii', 'ignore')
	    match = re.findall('\"typeStep\":\"[a-z]*\"', page)
	    if len(match) == 1:
		    lvlType = re.findall('"[a-z]"', match[0])
		    if len(lvlType) == 1:
			return lvlType[0][1]

    def isOilFinishedForToday(self):
        if self.isOldOil():
            response = self.session.get(self.config['siteUrl'] + 'neft/')

            tree = html.fromstring(response.text)
            return bool(tree.xpath("//div[@id='ventel_win']"))
	else:
	    pass

    def switchToOldOilType(self):
        self.session.post(self.config['siteUrl'] + 'neftlenin/', data={'action': 'hideNeftLEnin'})

    def isOldOil(self):
        response = self.session.get(self.config['siteUrl'] + 'neft/')

        return 'neftlenin' not in response.url

    def attack(self):
        if self.isOldOil():
            self.session.post(self.config['siteUrl'] + "alley/", data={'now': 0, 'action': "attack-npc3"})
	else:
	    self.session.post(self.config['siteUrl']+'alley/', data={
		'action': 'rest_cooldown',
		'code': 'tonus'
	    })
            self.session.post(self.config['siteUrl'] + "neftlenin/", data={'action': 'startAction'})

    def preMission(self):
        self.session.post(self.config['siteUrl'] + "neftlenin/", data={'action': 'preMissionView'})
        self.session.post(self.config['siteUrl'] + "neftlenin/", data={'action': 'preMission'})

    def getInfo(self):
	
        response = self.session.post(self.config['siteUrl'] + 'neftlenin/', data={
	    'action': 'getPrize'
	}, headers={'Accept': 'application/json'})

        print response.text.encode('ascii', 'ignore')
