#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Auto(object):
    def __init__(self, session, userConfig, carid):
        self.session = session
        self.config = userConfig
        self.carid = carid

    def bringup(self, points=9999):
        response = self.session.get(self.config['siteUrl']+'arbat/')
        if response.url == (self.config['siteUrl']+'arbat/'):
            tree = html.fromstring(response.text)

            timerBringUp = tree.xpath('//table[@class="process"]//td[@id="cooldown"]/@timer')

            if not timerBringUp:
                # look if enough fuel
                response = self.session.get(self.config['siteUrl']+'automobile/car/'+str(self.carid)+'/')
                tree = html.fromstring(response.text)

                fuel = unicode(tree.xpath('//div[@class="fuel"]/span/text()'))
                if unicode('0') in fuel:
                   self.session.post(self.config['siteUrl']+'automobile/buypetrol/'+str(self.carid)+'/', data={})


                self.session.post(self.config['siteUrl']+'automobile/bringup/', data={
                    'car': self.carid
                })
