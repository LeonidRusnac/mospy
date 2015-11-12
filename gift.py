#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Gift(object):
    # static constants
    EATCONST = {
        'tea': [],
        'chocolade': [],
        '15proc': [],
        '20proc': [],
        '25proc': [],
        '30proc': [],
        'neft': [1876968102, 1876968110, 1876968127, 1876968141, 1876968158, 1876968171]
    }

    BUYCONSTGIFTS = {
        'tea': [3860, 2936, 325, 327, 326],
        'chocolade': [3864, 2937, 328, 324, 323],
        'valuiki': [3351, 309],
        'respirators': [670, 671]
    }

    BUYCONSTDRUGS = {
        '15ruda': [84, 85, 86, 87, 88, 89],
        '25neft': [],  # depends by level
        '3ruda': []  # depends by level
    }

    def __init__(self, session, userConfig):
        self.session = session
        self.config = userConfig

    def buyGift(self, receiver, giftId, secret):
        response = self.session.post(self.config['siteUrl']+'shop/', data={
            'action': 'buy',
            'item': giftId,
            'playerid': receiver,
            'key': secret,
            'comment': ' ',
            'private': 'yes',
            'anonimous': 'yes'
        })

    def buyItem(self, itemid, secret, amount=1):
        response = self.session.post(self.config['siteUrl']+'shop/json/', data={
            'action': 'buy',
            'item': itemid,
            'key': secret,
            'amount': amount
        })

    def resetCooldown(self, resetby='tonus'):
        if resetby in ['tonus', 'snikers']:
            self.session.post(self.config['siteUrl']+'alley/', data={
                'action': 'rest_cooldown',
                'code': resetby
            })
        else:
            print "resetby is wrong, must be 'tonus' or 'snikers'"

    def eatDrugs(self, drugs=[]):
        for drug in drugs:
            self.session.get(self.config['siteUrl']+'player/json/use/'+drug)

    def buyGifts(self, receiver, gifts=[]):
        token = self.getSecret()
        for gift in gifts:
            self.buyGift(receiver, gift, token)

    def buyDrugs(self, drugs=[], amount=1):
        token = self.getSecret()
        for drug in drugs:
            self.buyItem(drug, token, amount)

    def getSecret(self):
        response = self.session.get(self.config['siteUrl']+'shop/section/gifts/#all')
        if response.url == (self.config['siteUrl']+"shop/section/gifts/#all"):
            tree = html.fromstring(response.text)
            return tree.xpath('//span[contains(@onclick,"Shop.checkAndBuy")]/@onclick')[0].split("'")[3]
        else:
            return ""

    def takePhoto(self, photoid, n):
        response = self.session.get(self.config['siteUrl']+"nightclub/photo/")

        if response.url == (self.config['siteUrl']+"nightclub/photo/"):
            for i in range(n):
                self.session.post(self.config['siteUrl']+"nightclub/setphoto/", data={
                    'action': 'setphoto',
                    'backid': photoid
                })
        else:
            print 'error setting phone'
