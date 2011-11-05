'''
Created on Nov 5, 2011

@author: David
'''
from plugin_base import PluginBase

class DatePlugin(PluginBase):
    PREFIX = "!"
    
    def plugin_init(self):
        self.register_event("channel_msg", self.on_channel_msg)
        
    def on_channel_msg(self, user, channel, msg):
        if msg.startswith(self.PREFIX):
            cmd = msg[len(self.PREFIX):]
            if cmd == "":
                return
            
            tokens = cmd.split(" ")
            cmd = tokens[0]
            if (len(tokens) > 1):
                args = tokens[1:]
            else:
                args = []
            
            self.dispatch_event("cmd_%s" % (cmd), [user, channel, cmd, args])