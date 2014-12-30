#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__ = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__ = "0.1"

import requests
from lxml import html


class Sovet(object):
    def __init__(self, session, userConfig):
        self.session = session
        self.config = userConfig

    def registerToGroup(self, lvl, password):
        # first of all check if not blocked in some place
        response = self.session.get(self.config['siteUrl']+'sovet/map/')

        if response.url == (self.config['siteUrl']+'sovet/map/'):
            # check if it's possible to register to game
            tree = html.fromstring(response.text)
            pr = tree.xpath('//span[@class="button big"]/@onclick')

            if pr:
                token = pr[0].split("'")[1]
                # select the right city
                self.session.post(self.config['siteUrl'] +
                                  'sovet/select_active_metro/', data={
                                      'action': 'select_active_metro',
                                      'metro': lvl})
                # now register do game
                self.session.post(self.config['siteUrl'] +
                                  'sovet/join_metro_fight/', data={
                                      'action': 'join_metro_fight',
                                      'metro': lvl,
                                      'type': 'metro',
                                      'joinkey': token})
                # now that I'm registered to fight let's enter to the group
                self.session.post(self.config['siteUrl'] +
                                  'groups/tryPasscode/', data={
                                      'action': 'tryPasscode',
                                      'type': 'sovet',
                                      'passcode': password})
                # now eat vitamins
                self.session.get(self.config['siteUrl'] +
                                 'player/json/use/1522031924/')
            else:
                print "can't register for sovet"
        else:
            print 'blocked in some place, can\'t register to sovet'
