'''
Created on Nov 1, 2011

@author: David Serrano
'''
class PluginBase(object):
    
    def __init__(self):
        pass
    
    def _set_bot_instance(self, bot):
        self.bot = bot;
        pass
    
    def on_op(self, user, channel, nick_oped):
        pass
    
    def on_deop(self, user, channel, nick_deoped):
        pass
    
    def on_voice(self, user, channel, nick_voiced):
        pass
    
    def on_devoice(self, user, channel, nick_devoiced):
        pass
    
    def on_channel_msg(self, user, channel, msg):
        pass
    
    def on_join(self, user, channel):
        pass
    
    def on_part(self, user, channel, msg):
        pass
    
    def on_priv_msg(self, user, msg):
        pass
    
    def on_kick(self, user, kicked_nick, chan, msg):
        pass
    
    def on_nick(self, user, new_nick):
        pass
    
    def on_quit(self, user, reason):
        pass
    
    def on_kill(self, user, reason):
        pass
    
    def on_numeric(self, event_num, nick, params, msg):
        pass
    
    def on_socket_closed(self):
        pass