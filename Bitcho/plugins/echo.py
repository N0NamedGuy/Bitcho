'''
Created on Nov 1, 2011

@author: David Serrano
'''
from plugin_base import PluginBase

class EchoPlugin(PluginBase):
    def __init__(self):
        print 'Loaded'
        pass
    
    def on_channel_msg(self, user, channel, msg):
        print "<%s@%s> %s" % (user,channel,msg);
        self.bot.send_msg(channel, "Hi %s" % (user))
        
    def on_join(self, user, channel):
        self.bot.send_msg(channel, "Welcome to %s, %s!" % (channel, user))