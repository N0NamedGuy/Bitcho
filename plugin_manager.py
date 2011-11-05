'''
Created on Nov 5, 2011

@author: David
'''
import os
import json
from plugin_base import PluginBase
from fun_thread import FunThread
PLUGIN_PATH = 'plugins'

# TODO: put plugin management in its own module
# code from:
# http://www.luckydonkey.com/2008/01/02/python-style-plugins-made-easy/
def get_plugins(bot):
    plugins = {}
    try:
        f = open("plugins/conf/blacklist.json")
        blacklist = json.load(f)['blacklist']
        f.close()
    except Exception:
        blacklist = []
    
    def add_subclass(modulename):
        
        name = ".".join(modulename.split(".")[1:])
        
        if name in blacklist:
            print "Plugin %s blacklisted" % (name,)
            return
            
        def add_plugin(e):
            print "Adding plugin %s" % (name,) 
            
            e._set_bot_instance(bot)
            e.plugin_init()
            evs = e.events
            
            for ev in evs:
                if not ev in plugins:
                    plugins[ev] = []
                    
                plugins[ev].append(e)
        
        module=__import__(modulename)
 
        #walk the dictionaries to get to the last one
        d=module.__dict__
        for m in modulename.split('.')[1:]:
            d=d[m].__dict__
 
        for key, entry in d.items():
            if key == PluginBase.__name__: #@UndefinedVariable
                continue
 
            try:
                if issubclass(entry, PluginBase): 
                    add_plugin(entry())
            except TypeError:
                continue
    
    
    for root, dirs, files in os.walk(PLUGIN_PATH): #@UnusedVariable
        for name in files:
            if name.endswith(".py") and not name.startswith("__"):
                path = os.path.join(root, name)
                modulename = path.rsplit('.', 1)[0].replace(os.sep, '.')
                add_subclass(modulename)
    
    bot._plugins = plugins

def handle_plugin(event, plugin, args):
    if not event in plugin.events:
        return
    
    funs = plugin.events[event]
    
    for ev in funs:
        t = FunThread(ev.callback, args)
        t.start()
        
        # TODO: some kind of thread manager would be nice =)

def handle_plugins(bot, event, args = []):
    if not event in bot._plugins:
        return
    
    plugs = bot._plugins[event]
    for p in plugs:
        handle_plugin(event, p, args)