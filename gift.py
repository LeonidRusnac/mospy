#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Gift(object):
    def __init__(self, session, userConfig):
        self.session = session
        self.config = userConfig

    def makeGift(self, receiver, giftId):
        # grab the user details whom to send the gift

        # get token
        response = self.session.get(self.config['siteUrl']+"shop/section/gifts/#all")

        if response.url == (self.config['siteUrl']+"shop/section/gifts/#all"):
            #get info of the player search info inside the response.text

            print "ook"
            tree = html.fromstring(response.text)

            # onClick Shop.checkAndBuy
            # //a[contains(@onclick,"alleyAttack")]/@onclick

            token = tree.xpath('//span[contains(@onclick,"Shop.checkAndBuy")]/@onclick')[0].split("'")[3]

            response = self.session.post(self.config['siteUrl']+'shop/', data={
                'action': 'buy',
                'item': giftId,
                'playerid': receiver,
                'key': token,
                'comment': ' ',
                'private': 'yes',
                'anonimous': 'yes'
            })

        else:
            print "error gifts"

    def buyItem(self, itemid, section):
        response = self.session.get(self.config['siteUrl']+"shop/section/"+section+"/")

        if response.url == (self.config['siteUrl']+"shop/section/"+section+"/"):
            tree = html.fromstring(response.text)

            token = tree.xpath('//span[contains(@onclick,"Shop.checkAndBuy")]/@onclick')[0].split("'")[3]

            response = self.session.post(self.config['siteUrl']+'shop/json/', data={
                'action': 'buy',
                'item': itemid,
                'key': token,
            })

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
