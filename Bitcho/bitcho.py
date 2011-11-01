'''
Created on Nov 1, 2011

@author: David Serrano
'''
from ircclient import ircclient
from plugin_base import PluginBase
import os

class bitcho(ircclient):
    PLUGIN_PATH = 'plugins'
    
    def reload_plugins(self):
        self.plugins = []
        
        def add_subclass(modulename):
            module=__import__(modulename)
     
            #walk the dictionaries to get to the last one
            d=module.__dict__
            for m in modulename.split('.')[1:]:
                d=d[m].__dict__
     
            #look through this dictionary for things
            #that are subclass of Job
            #but are not Job itself
            for key, entry in d.items():
                if key == PluginBase.__name__:
                    continue
     
                try:
                    if issubclass(entry, PluginBase):
                        self.plugins.append(entry())
                except TypeError:
                    #this happens when a non-type is passed in to issubclass. We
                    #don't care as it can't be a subclass of Job if it isn't a
                    #type
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
        ircclient.send_all(self,
                           [
                            'USER bitcho %s bla :hihi' % (ircclient.get_host(self),) ,
                            "nickserv login %s %s" % (self.auth[0], self.auth[1])])

    def join_channels(self):
        for chan in self.ajoin:
            ircclient.join(self,chan)
        
    def event_channel_msg(self, user, channel, msg):
        for p in self.plugins:
            p.on_channel_msg(user, channel, msg)
