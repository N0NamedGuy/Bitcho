'''
Created on May 31, 2013

@author: David Serrano
'''
import json
import sys
from plugin_base import PluginBase
from ircclient import IRCClient

class AuthPlugin(PluginBase):
    auth = {}

    def plugin_init(self):
        self.register_event("init", self.on_init)
        try:
            f = open("plugins/conf/auth.json")
            self.auth = json.load(f)
            f.close
        except Exception as e:
            self.auth["nick"] = ""
            self.auth["username"] = ""
            self.auth["host"] = ""
            self.auth["realname"] = ""
            self.auth["commands"] = []

    def on_init(self):
        user_cmd = 'USER %s %s %s :%s' %  \
            (self.auth["username"].encode('utf-8'), \
                self.auth["host"].encode('utf-8'), \
                self.auth["host"].encode('utf-8'), \
                self.auth["realname"].encode('utf-8')
             )

        nick_cmd = 'NICK ' + self.auth["nick"].encode('utf-8')

        other_cmd = self.auth["commands"]

        self.bot.send_all([user_cmd, nick_cmd])
        self.bot.send_all(other_cmd)
        
