'''
Created on Nov 1, 2011

@author: David Serrano
'''

class PluginEvent():
    def __init__(self):
        self.callback = lambda : {}
        self.event_generic = ''
    
class PluginBase(object):
    
    def __init__(self):
        self.events = {}
        pass
    
    def plugin_init(self):
        pass
    
    def register_event(self, event_generic, callback):
        e = PluginEvent()
        e.callback = callback
        e.event_generic = event_generic
        
        if not event_generic in self.events:
            self.events[event_generic] = []
        
        self.events[event_generic].append(e)
        
    def dispatch_event(self, event_generic, args):
        import plugin_manager
        plugin_manager.handle_plugins(self.bot, event_generic, args)
    
    def unregister_event(self, event_generic):
        if event_generic in self.events:
            del self.events[event_generic]
    
    def unregister_callback(self, event_generic, callback):
        if not event_generic in self.events:
            return
        
        for e in self.events[event_generic]:
            if e.callback == callback:
                del self.events[e]
                break
    
    def _set_bot_instance(self, bot):
        self.bot = bot;
        pass
