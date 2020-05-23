#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__   = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__   = "0.1"

import requests
from lxml import html

class Attack(object):
    '''A class that contains methods for attacks'''

    def __init__(self, session, userConfig):
        self.session = session
        self.config = userConfig

    def attack(self, typeA='', min=0, max=0, id=0, npc=True, clanwar=False):
        '''
        if id attack by id, if not type attack by levels
        else attack by type
        '''
        if id != 0:
            print 'Attack by id'
            d = {'action': 'attack', 'player': id, 'werewolf': 0, 'useitems': 0}
            if clanwar:
                # d['test'] = True
                pass
            response = self.session.post(self.config['siteUrl']+'alley/', data=d)

            if 'fight' in response.url:
                tree = html.fromstring(response.text)
                turghi = tree.xpath('//span[@class="tugriki"]/text()')
                if len(turghi) > 0:
                    return int(turghi[0].translate(None, ','))
                else:
                    return 0
            else:
		return -1

        elif typeA == '':
            print 'Attack by levels'
            response = self.session.post(self.config['siteUrl']+'alley/search/level/', data={
                'minlevel': min,
                'maxlevel': max
            })
            if 'alley/search' in response.url:
                tree = html.fromstring(response.text)
                victimID = 0
                victimID = tree.xpath('//a[contains(@onclick,"alleyAttack")]/@onclick')[0]
                victimID = victimID.split('(')[1].split(',')[0]
                #print victimID
                self.attack(id=victimID)
        else:
            print 'Attack by type'
            types = 'equal' , 'weak' , 'strong' , 'enemy' , 'victim'
            if typeA not in types:
                typeA = types[1]

            response = self.session.post(self.config['siteUrl']+'alley/search/type/', data={
                'type': typeA,
                'werewolf': 0
            })

            if 'alley/search' in response.url:
                tree = html.fromstring(response.text)

                if max > -1:
                    i = 0
                    while i<100:
                        i += 1
                        valid = not npc
                        victimLvl = tree.xpath('//div[@class="fighter2"]//span[@class="level"]/text()')[0]
                        victimLvl = int(victimLvl.split('[')[1].split(']')[0])
                        victimID = 0

                        nnn = tree.xpath('//div[@class="fighter2"]//i/@class')[0]
                        print nnn
                        if nnn == 'npc':
                            valid = True
                        if valid and (victimLvl <= max) and (victimLvl >= min):
                            break
                        response = self.session.get(self.config['siteUrl']+'alley/search/again/')
                        tree = html.fromstring(response.text)
                        if i > 99:
                            return ''
                else:
                    victimLvl = tree.xpath('//div[@class="fighter2"]//span[@class="level"]/text()')[0]
                    victimLvl = victimLvl.split('[')[1].split(']')[0]

                victimID = tree.xpath('//a[contains(@onclick,"alleyAttack")]/@onclick')[0]
                victimID = victimID.split('(')[1].split(',')[0]
                #print victimID
                self.attack(id=victimID)
            else:
                print 'Error'


