'''
Created on Nov 5, 2011

@author: David
'''
import json
from plugin_base import PluginBase

def get_conf():
    f = open("plugins/conf/commands.json")
    conf = json.load(f)
    f.close()
    return conf

def get_prefix():
    return get_conf()["prefix"]

def check_permission(command, user):
    conf = get_conf()
    perms = conf['permissions'] #@UnusedVariable
    masters = conf['masters']
    
    # TODO: do me right please...
    if user.nick in masters:
        return True
    
    return False

class CommandsPlugin(PluginBase):
    
    def plugin_init(self):
        self.register_event("channel_msg", self.on_channel_msg)
        
    def on_channel_msg(self, user, channel, msg):
        prefix = get_prefix()
        if msg.startswith(prefix):
            cmd = msg[len(prefix):]
            if cmd == "":
                return
            
            tokens = cmd.split(" ")
            cmd = tokens[0]
            
            if not(check_permission(cmd, user)):
                return
            
            if (len(tokens) > 1):
                args = tokens[1:]
            else:
                args = []
            
            self.dispatch_event("cmd_%s" % (cmd), [user, channel, cmd, args])