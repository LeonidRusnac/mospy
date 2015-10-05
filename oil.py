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
        print 'bazinga'
        response = self.session.get(self.config['siteUrl'] + "neftlenin/")

        tree = html.fromstring(response.text)
        progress = tree.xpath('//div[@class="progress-wrapper"]//i[@class="counter"]/text()')[0]
        return progress

    def getCurrentLevelNumber(self):
        pass

    def getCurrentLevelType(self):
        pass
