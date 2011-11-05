'''
Created on Nov 1, 2011

@author: David Serrano
'''
from plugin_base import PluginBase

class WelcomePlugin(PluginBase):
    def plugin_init(self):
        self.register_event("join", self.on_join)
        
    def on_join(self, user, channel):
        self.bot.send_msg(channel, "Welcome to %s, %s!" % (channel, user))