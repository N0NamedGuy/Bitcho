'''
Created on Nov 6, 2011

@author: David
'''
from plugin_base import PluginBase
from fun_thread import FunThread
import sys

class ConsolePlugin(PluginBase):
    def work(self):
        while True:
            sys.stdout.write("> ")
            line = sys.stdin.readline()
            
            if line == "": return
            line = line[:-2]
        
            if line.startswith("/"):
                line = line[1:]
                self.bot.send(line)
        
    def plugin_init(self):
        # TODO: Process more events
        self.register_event("connect", self.run_it)
        self.register_event("channel_msg", self.on_channel_msg)
        self.register_event("priv_msg", self.on_priv_msg)
        
        self.register_event("join", self.on_join)
        self.register_event("part", self.on_part)
        
        self.register_event("numeric", self.on_numeric)
        
    def run_it(self):
        FunThread(self.work, []).start()
    
    def on_join(self, user, channel):
        print "* %s joined %s" % (user, channel)
    
    def on_part(self, user, channel, msg):
        print "* %s left %s (%s)" % (user, channel, msg)
        
    def on_channel_msg(self, user, channel, msg):
        print "<%s@%s> - %s" % (user, channel, msg)
        
    def on_priv_msg(self, user, msg):
        print "<%s> - %s" % (user, msg)

    def on_numeric(self, user, *tokens):
        print tokens