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
    BUY_CONST_GIFTS = {
        'tea': [3860, 2936, 325, 327, 326],
        'chocolade': [3864, 2937, 328, 324, 323],
        'valuiki': [3351, 309],
        'respirators': [670, 671]
    }

    DRUGS_CONST = {
        '15ruda': [84, 85, 86, 87, 88, 89],
        '25neft': [3060, 3061, 3062, 3063, 3064, 3065],  # 17 level
        '9ruda': [3054, 3055, 3056, 3057, 3058, 3059],  # 17 level
        '3ruda': [2609, 2610, 2611, 2612, 2613, 2614],  # 17 level
        'tea': [3861, 3862, 3863, 2941, 2942, 2943, 234, 235, 236, 231, 232, 233, 228, 229, 230],
        'chocolate': [3865, 3866, 3867, 2938, 2939, 2940, 222, 223, 224, 219, 220, 221, 216, 217, 218],
        'lolipopAnti': [2872],
        'lolipopPro': [2871],
        'piani': [52],
        'tvorog': [53]
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
        ids = [self.getIdByDataSt(drug) for drug in drugs]
        for drug in ids:
            self.session.get(self.config['siteUrl']+'player/json/use/'+str(drug))

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

    def getIdByDataSt(self, dataST):
        response = self.session.get(self.config['siteUrl']+'player/')
        if response.url == (self.config['siteUrl']+'player/'):
            tree = html.fromstring(response.text)
            return tree.xpath('//img[@data-st='+str(dataST)+']/@data-id')[0]
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
