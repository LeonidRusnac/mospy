#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Leonid Rusnac <leonidrusnac4 at gmail.com>"
__license__ = "MIT"
__copyright__ = "Copyright 2014, Leonid Rusnac"
__version__ = "0.1"

import ast
import codecs


class Chat(object):
    def __init__(self, session, userConfig):
        self.session = session
        self.config = userConfig

    def getSystemMessages(self, lastID, pathToSave):
        messages = ast.literal_eval(self.session.post(
            self.config['siteUrl']+'/chat/get-messages/', data={
                'lastMessageId': lastID
            }).text)['result']['messages']

        for m in messages:
            lastID = messages[m]['id']
            if messages[m]['type'] == 'system':
                messTime = messages[m]['time']
                mess = (messages[m]['message']).decode('utf8')
                finalMess =  messTime + ': (' + lastID + ') ' + mess

                with codecs.open(pathToSave, "a", "utf-8") as stream:   # or utf-8
                        stream.write(finalMess + u"\n\n")

        return lastID
