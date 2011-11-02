'''
Created on Nov 2, 2011

@author: David Serrano
'''
from plugin_base import PluginBase

class TwitterPlugin(PluginBase):
    
    def plugin_init(self):
        self.register_event("connect", self.on_connect)
    
    def on_connect(self):
        pass