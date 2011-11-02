'''
Created on Nov 1, 2011

@author: David Serrano
'''
from plugin_base import PluginBase

class EchoPlugin(PluginBase):
    def register_events(self):
        self.register_event("channel_msg", self.on_channel_msg)
        self.register_event("join", self.on_join)
        self.register_event("priv_msg", self.on_priv_msg)

    def on_channel_msg(self, user, channel, msg):
        self.bot.send_msg(channel, "Hi %s" % (user))
        
    def on_priv_msg(self, user, msg):
        self.bot.send_msg(str(user), 'You are a fag!')
        
    def on_join(self, user, channel):
        self.bot.send_msg(channel, "Welcome to %s, %s!" % (channel, user))