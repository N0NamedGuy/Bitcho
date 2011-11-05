'''
Created on Nov 5, 2011

@author: David Serrano
'''
import json
import sys
from plugin_base import PluginBase

class JoinPlugin(PluginBase):
    def plugin_init(self):
        self.register_event("cmd_ajoin", self.on_cmd_ajoin)
        self.register_event("cmd_join", self.on_cmd_join)
        self.register_event("cmd_part", self.on_cmd_part)
        self.register_event("connect", self.do_ajoin)
        
    def on_ajoin(self, user, channel, cmd, args):
        self.do_ajoin()
    
    def on_cmd_ajoin(self, user, channel, cmd, args):
        self.do_ajoin()
    
    def on_cmd_join(self, user, channel, cmd, args):
        if len(args) == 1:
            self.bot.join(args[0])
        
    def on_cmd_part(self, user, channel, cmd, args):
        msg = ""
        if len(args) > 1:
            msg = " ".join(args[1:])
            
        self.bot.part(args[0], msg)
    
    def do_ajoin(self):
        try: 
            f = open("plugins/conf/autojoin.json")
            ajoin = json.load(f)["autojoin"]
            f.close()
            
        except Exception:
            ajoin= []
        
        if len(sys.argv) >= 4:
            ajoin += sys.argv[3:]
        
        for chan in ajoin:
            self.bot.join(chan)