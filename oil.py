#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__ = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__ = "0.1"

from lxml import html


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
            # $.post('http://www.moswar.ru/neftlenin', {"action": "getPrize"})
            pass

    def getCurrentLevelType(self):
        if self.isOldOil():
            return 'attack'
        else:
            pass

    def isOilFinishedForToday(self):
        if self.isOldOil():
            response = self.session.get(self.config['siteUrl'] + 'neft/')

            tree = html.fromstring(response.text)
            return bool(tree.xpath("//div[@id='ventel_win']"))

    def switchToOldOilType(self):
        self.session.post(self.config['siteUrl'] + 'neftlenin/', data={'action': 'hideNeftLEnin'})

    def isOldOil(self):
        response = self.session.get(self.config['siteUrl'] + 'neft/')

        return 'neftlenin' not in response.url

    def attack(self):
        if self.isOldOil():
            self.session.post(self.config['siteUrl'] + "alley/", data={'now': 0, 'action': "attack-npc3"})
