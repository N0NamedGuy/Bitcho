'''
Created on Nov 1, 2011

@author: David Serrano
'''
from ircclient import ircclient
import plugin_manager

class Bitcho(ircclient):

    def __init__(self, host, port, auth, ajoin):
        ircclient.__init__(self, host, port)
        self.auth = auth
        self.ajoin = ajoin
        plugin_manager.get_plugins(self)
        
    def send_welcome(self):
        ircclient.send_all(self, [
            'USER Bitcho %s bla :hihi' % (ircclient.get_host(self),) ,
            "nickserv login %s %s" % (self.auth[0], self.auth[1])])

    def join_channels(self):
        for chan in self.ajoin:
            ircclient.join(self,chan)
    
    def recv_loop(self):
        plugin_manager.handle_plugins(self, "connect")
        return ircclient.recv_loop(self)
    
    def event_join(self, user, channel):
        ircclient.event_join(self, user, channel)
        plugin_manager.handle_plugins(self, 'join', [user, channel])
        
    def event_channel_msg(self, user, channel, msg):
        ircclient.event_channel_msg(self, user, channel, msg)
        plugin_manager.handle_plugins(self, 'channel_msg', [user, channel, msg])
    
    def event_priv_msg(self, user, msg):
        ircclient.event_priv_msg(self, user, msg)
        plugin_manager.handle_plugins(self, 'priv_msg', [user, msg])
    
    def event_op(self, user, channel, nick_oped):
        ircclient.event_deop(self, user, channel, nick_oped)
        plugin_manager.handle_plugins(self, 'op', [user, channel, nick_oped])
        
    def event_deop(self, user, channel, nick_deoped):
        ircclient.event_deop(self, user, channel, nick_deoped)
        plugin_manager.handle_plugins(self, 'deop', [user, channel, nick_deoped])
        
    # TODO: other events
    
    def event_raw(self, tokens, raw):
        if len(tokens[1]) < 3:
            return
        
        ev = tokens[1].lower()
        
        if not ev.isdigit():
            if not ev in self._plugins:
                return
            
            plugs = self._plugins[ev]
            for p in plugs:
                plugin_manager.handle_plugin('raw', p, tokens)
                