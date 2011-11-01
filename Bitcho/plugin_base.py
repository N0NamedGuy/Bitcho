'''
Created on Nov 1, 2011

@author: David Serrano
'''
class PluginBase(object):
    
    def __init__(self):
        pass
    
    def on_channel_msg(self, user, channel, msg):
        pass