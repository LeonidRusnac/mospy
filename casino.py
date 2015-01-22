#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Casino(object):
    def __init__(self, session, userConfig):
        self.session = session
        self.config = userConfig

    def playBlackjack(self, bet=30, min=17):
        #self.session.post(self.config['siteUrl']+'casino/blackjack/', data={'action':'get'})
        response = self.session.post(self.config['siteUrl']+'casino/blackjack/',
                                     data={
                                         'action': 'new',
                                         'bet': 30})
        print response.text
        #tree = html.fromstring(response.text)
        #val = tree.xpath('//div[@class="area player first current"]/div[@class="info"]/span[@class="total"]/span/text()')[0]
        #print val
