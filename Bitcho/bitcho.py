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
        self.plugins = {}
        
        
        def add_subclass(modulename):
        
            def add_plugin(e):
                e._set_bot_instance(self)
                e.register_events()
                evs = e.events
                
                for ev in evs:
                    if not ev in self.plugins:
                        self.plugins[ev] = []
                        
                    self.plugins[ev].append(e)
            
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
                        add_plugin(entry())
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
        print self.plugins
        
    def send_welcome(self):
        ircclient.send_all(self, [
            'USER bitcho %s bla :hihi' % (ircclient.get_host(self),) ,
            "nickserv login %s %s" % (self.auth[0], self.auth[1])])

    def join_channels(self):
        for chan in self.ajoin:
            ircclient.join(self,chan)
        
    def handle_plugin(self, event, plugin, args):
        if not event in plugin.events:
            return
        
        evs = plugin.events[event]
        
        for ev in evs:
            ev.callback(*args)
    
    def handle_plugins(self, event, args):
        if not event in self.plugins:
            return
        
        plugs = self.plugins[event]
        for p in plugs:
            self.handle_plugin(event, p, args)
    
    def event_join(self, user, channel):
        ircclient.event_join(self, user, channel)
        self.handle_plugins('join', [user, channel])
        
    def event_channel_msg(self, user, channel, msg):
        ircclient.event_channel_msg(self, user, channel, msg)
        self.handle_plugins('channel_msg', [user, channel, msg])
    
    def event_priv_msg(self, user, msg):
        ircclient.event_priv_msg(self, user, msg)
        self.handle_plugins('priv_msg', [user, msg])
    
    def event_op(self, user, channel, nick_oped):
        ircclient.event_deop(self, user, channel, nick_oped)
        self.handle_plugins('op', [user, channel, nick_oped])
        
    def event_deop(self, user, channel, nick_deoped):
        ircclient.event_deop(self, user, channel, nick_deoped)
        self.handle_plugins('deop', [user, channel, nick_deoped])
        
    
    def event_raw(self, tokens, raw):
        if len(tokens[1]) < 3:
            return
        
        ev = tokens[1].lower()
        
        if not ev.isdigit():
            if not ev in self.plugins:
                return
            
            plugs = self.plugins[ev]
            for p in plugs:
                self.handle_plugin('raw', p, tokens)
                