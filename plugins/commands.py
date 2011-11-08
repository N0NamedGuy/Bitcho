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


# Lower permissions have higher precedence
class CommandsPlugin(PluginBase):
    
    def plugin_init(self):
        self.conf = get_conf()
        self.register_event("channel_msg", self.on_channel_msg)

    def check_permission(self, command, user, channel):
        """
        Checks if a command can be run by a certain user on a certain channel
        """
        perm_map = {"voice": "+", "op": "@", "all" : ""}
        
        # If the command is not set in the permissions, it is assumed
        # that the command can be used by anyone
        if command in self.conf['permissions']: 
            cmd_perm = [command]
        else:
            return True
        
        # Now with the permission check
        user_status = self.bot.get_user_status(channel, user.get_nick())
        cmd_status = perm_map[cmd_perm]
        
        return (cmd_perm == "all" or (user.get_nick() in self.conf['masters'])) \
            or (user_status == '@' and
                (cmd_status == '@' or cmd_status == '+' or cmd_status == '')) \
            or (user_status == '+' and
                (cmd_status == '+' or cmd_status == '')) \
            or (user_status == cmd_status)
        
    def on_channel_msg(self, user, channel, msg):
        # FIXME: Sometime this stops working on the presence of strange stuff
        prefix = self.conf['prefix']
        if msg.startswith(prefix):
            cmd = msg[len(prefix):]
            if cmd == "":
                return
            
            tokens = cmd.split(" ")
            cmd = tokens[0]
            
            if not(self.check_permission(cmd, user, channel)):
                return
            
            if (len(tokens) > 1):
                args = tokens[1:]
            else:
                args = []
            
            self.dispatch_event("cmd_%s" % (cmd), [user, channel, cmd, args])