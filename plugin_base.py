'''
Created on Nov 1, 2011

@author: David Serrano
'''
class PluginEvent():
    def __init__(self):
        self.callback = lambda : {}
        self.event = ''
    
class PluginBase(object):
    
    def __init__(self):
        self.events = {}
        pass
    
    def plugin_init(self):
        pass
    
    def register_event(self, event, callback):
        print "Registering " + event
        
        e = PluginEvent()
        e.callback = callback
        e.event = event
        
        if not event in self.events:
            self.events[event] = []
        
        self.events[event].append(e)
    
    def unregister_event(self, event):
        if not event in self.events:
            return
        
        del self.events[event]
    
    def unregister_callback(self, event, callback):
        if not event in self.events:
            return
        
        for e in self.events[event]:
            if e.callback == callback:
                del self.events[e]
                break
    
    def _set_bot_instance(self, bot):
        self.bot = bot;
        pass
