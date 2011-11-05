'''
Created on Nov 5, 2011

@author: David Serrano
'''
import json
import sys
from plugin_base import PluginBase

class AjoinPlugin(PluginBase):
    def plugin_init(self):
        self.register_event("cmd_ajoin", self.on_command)
        self.register_event("connect", self.do_ajoin)
    
    def on_command(self, user, channel, cmd, args):
        self.do_ajoin()
    
    def do_ajoin(self):
        try: 
            f = open("plugins/conf/autojoin")
            ajoin = json.load(f)["autojoin"]
            f.close()
            
        except Exception:
            ajoin= []
        
        if len(sys.argv) >= 4:
            ajoin += sys.argv[3:]
        
        
        for chan in ajoin:
            self.bot.join(chan)