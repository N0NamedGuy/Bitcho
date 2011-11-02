'''
Created on Nov 2, 2011

@author: David Serrano
'''
from plugin_base import PluginBase
from threading import Timer

class TwitterPlugin(PluginBase):
    
    def plugin_init(self):
        self.register_event("connect", self.on_connect)
    
    def on_connect(self):
        t = Timer(3, self.do_it)
        t.start()
    
    def do_it(self):
        try:
            self.bot.send_msg("#bot-events", "derp")
        except Exception, e:
            print e
        
        t = Timer(3, self.do_it)
        t.start()