'''
Created on Nov 5, 2011

@author: David Serrano
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

def has_access(bot, user, permission, channel, masters):
    # pure copy pasta from the last version, ihih
    # it is ugly, I know...
    
    perm_map={'all': '*', 'voice': '+', 
                'op': '@', 'master': 'M'}
    perm = perm_map[permission]
    
    user_perm = '*'
    # firstly and foremost: can i run this?
    # FIXME: If the message is private, how should bot check for permissions?
    if user.get_nick() in masters:
        user_perm = 'M'
    elif channel != None:
        user_perm = bot.get_users(self,channel)[user.get_nick()].get_status()
    
    return not(not (user.get_nick() in masters and user_perm == 'M')) \
        and (not (perm == '@' and user_perm == '@')) \
        and (not (perm == '+' and ((user_perm == '@') 
                                         or (user_perm == '+') 
                                         or (user_perm == 'M')))) \
        and (not (perm == '*'))

# Lower permissions have higher precedence
def check_permission(bot, command, user, channel):
    conf = get_conf()
    perms = conf['permissions']
    masters = conf['masters']
    
    if command in perms['all']:
        return True
    elif command in perms['voice']:
        return has_access(bot, user, 'voice', channel, masters)
    elif command in perms['op']:
        return has_access(bot, user, 'op', channel, masters)
    elif command in perms['master']:
        return has_access(bot, user, 'master', channel, masters)
    
    return True

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
            
            if not(check_permission(self.bot, cmd, user, channel)):
                return
            
            if (len(tokens) > 1):
                args = tokens[1:]
            else:
                args = []
            
            self.dispatch_event("cmd_%s" % (cmd), [user, channel, cmd, args])