#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Auto(object):
    def __init__(self, session, userConfig, carid, direction='None'):
        self.session = session
        self.config = userConfig
        self.carid = carid
        self.direction = direction

    def bringup(self, points=9999):
        response = self.session.get(self.config['siteUrl']+'arbat/')
        if response.url == (self.config['siteUrl']+'arbat/'):
            tree = html.fromstring(response.text)

            timerBringUp = tree.xpath('//table[@class="process"]//td[@id="cooldown"]/@timer')

            if not timerBringUp:
                self.buyPetrol()

                self.session.post(self.config['siteUrl']+'automobile/bringup/', data={
                    'car': self.carid
                })

    def ride(self, direction='None'):
        if not direction:
            if not self.direction:
                return
            else:
                direction = self.direction

        self.buyPetrol()

        response = self.session.post(self.config['siteUrl']+'automobile/ride/',
                                     data = {
                                        'direction': direction,
                                        'car': self.carid
                                     })

    def buyPetrol(self):
        response = self.session.get(self.config['siteUrl']+'automobile/car/'+str(self.carid)+'/')
        tree = html.fromstring(response.text)

        fuel = unicode(tree.xpath('//div[@class="fuel"]/span/text()'))
        if unicode('0/5') in fuel:
            self.session.post(self.config['siteUrl']+'automobile/buypetrol/'+str(self.carid)+'/', data={})
