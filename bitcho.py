'''
Created on Nov 1, 2011

This is the implementation of an IRCClient class called Bitcho.

@author: David Serrano
'''
from ircclient import IRCClient
import plugin_manager

class Bitcho(IRCClient):
    """
    An IRCClient implementation, that calls plugin methods.
    """

    def __init__(self, host, port=6667):
        """
        Makes a connection to an IRC server.
        
        host - the IRC server's host
        port - the IRC server's listening port
        """
        IRCClient.__init__(self, host, port)
        plugin_manager.get_plugins(self)
    
    def recv_loop(self):
        """
        Runs the event system. This method is a blocking one.
        """
        plugin_manager.handle_plugins(self, "init")
        plugin_manager.handle_plugins(self, "connect")
        return IRCClient.recv_loop(self)
    
    def event_generic(self, event_generic, args):
        IRCClient.event_generic(self, event_generic, args)
        plugin_manager.handle_plugins(self, event_generic, args)
                
