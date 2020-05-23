#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from time import sleep


class HuntClub(object):
    '''A class that scans and attacks in hunt'''

    def __init__(self, session, userConfig):
        self.session = session
        self.config = userConfig

    def numattacks(self):
        # return the numbers of remaining attacks
        response = self.session.get(self.config['siteUrl'] + 'huntclub/')
        tree = html.fromstring(response.text)
        ris = tree.xpath('//div[@class="prolong"]//p[@class="holders"]/text()')[0]
        ris = ris.split(': ')[1]
        return int(ris)

    def hunt(self, level, at, timers=('',''), resetby='tonus'):
        i = 0
        done = False
        while not done and i < 20:
            response = self.session.get(self.config['siteUrl'] + 'huntclub/')
            tree = html.fromstring(response.text)

            ris = tree.xpath('//table[@class="list"]//span[@class="user "]/a[starts-with(@href, "/player")]/@href')
            if ris != []:
                myhp = tree.xpath('//div[@id="personal"]//span[@id="currenthp"]/text()')[0]
                myhp = int(myhp)

            for r in set(ris):
                r = r.split('/')[2]

                response = self.session.get(
                    self.config['siteUrl'] + 'player/' + r)
                tree = html.fromstring(response.text)
                lvl = tree.xpath('//h3[@class="curves clear"]//span[@class="level"]/text()')
		if len(lvl) > 0:
                    lvl = lvl[0]
		else:
                    lvl = tree.xpath('//div[@class="heading clear custom-profile__header"]//span[@class="user "]//span[@class="level"]/text()')
                lvl = int(str(lvl[1]) + str(lvl[2]))

                hp = tree.xpath('//div[@class="pers enemy"]//span[@class="currenthp"]/text()')
                if hp != []:
                    hp = int(hp[0])

                    if lvl in level and hp < (0.95 * myhp):
                        # attack by id = r
                        if timers != ('',''):
                            # eat snikers
                            self.session.post(self.config['siteUrl']+'alley/', data={
                                'action': 'rest_cooldown',
                                'code': resetby
                            })
                        at.attack(id=r)
                        done = True
                        break
            sleep(1)
            i = i + 1
