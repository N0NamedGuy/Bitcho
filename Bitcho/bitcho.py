'''
Created on Nov 1, 2011

@author: David Serrano
'''
from ircclient import ircclient
from plugin_base import PluginBase
import os

class bitcho(ircclient):
    PLUGIN_PATH = 'plugins'
    
    # code from:
    # http://www.luckydonkey.com/2008/01/02/python-style-plugins-made-easy/
    def reload_plugins(self):
        self.plugins = []
        
        def add_subclass(modulename):
            module=__import__(modulename)
     
            #walk the dictionaries to get to the last one
            d=module.__dict__
            for m in modulename.split('.')[1:]:
                d=d[m].__dict__
     
            for key, entry in d.items():
                if key == PluginBase.__name__:
                    continue
     
                try:
                    if issubclass(entry, PluginBase):
                        e = entry()
                        e._set_bot_instance(self);
                        self.plugins.append(e)
                except TypeError:
                    continue
        
        
        for root, dirs, files in os.walk(self.PLUGIN_PATH):
            for name in files:
                if name.endswith(".py") and not name.startswith("__"):
                    path = os.path.join(root, name)
                    modulename = path.rsplit('.', 1)[0].replace(os.sep, '.')
                    add_subclass(modulename)
        
    
    def __init__(self, host, port, auth, ajoin):
        ircclient.__init__(self, host, port)
        self.auth = auth
        self.ajoin = ajoin
        self.reload_plugins()
        
    def send_welcome(self):
        ircclient.send_all(self, [
            'USER bitcho %s bla :hihi' % (ircclient.get_host(self),) ,
            "nickserv login %s %s" % (self.auth[0], self.auth[1])])

    def join_channels(self):
        for chan in self.ajoin:
            ircclient.join(self,chan)
        
    def event_channel_msg(self, user, channel, msg):
        for p in self.plugins:
            p.on_channel_msg(user, channel, msg)
            
    def event_join(self, user, channel):
        for p in self.plugins:
            p.on_join(user, channel)