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

    # TODO: when moving send_welcome to its own plugin
    # move auth parameter along with it
    def __init__(self, host, port=6667, auth=[]):
        """
        Makes a connection to an IRC server.
        
        host - the IRC server's host
        port - the IRC server's listening port
        auth - an array containing auth information (soon to be removed)
        """
        IRCClient.__init__(self, host, port)
        self.auth = auth
        plugin_manager.get_plugins(self)
    
    # TODO: move to a plugin of its own
    def send_welcome(self):
        """
        Sends the welcome message to the connected IRC server.
        (soon to be removed)
        """
        IRCClient.send_all(self, [
            'USER Bitcho %s bla :hihi' % (IRCClient.get_host(self),) ,
            "nickserv login %s %s" % (self.auth[0], self.auth[1])])

    def recv_loop(self):
        """
        Runs the event system. This method is a blocking one.
        """
        plugin_manager.handle_plugins(self, "connect")
        return IRCClient.recv_loop(self)
    
    def event_generic(self, event_generic, args):
        IRCClient.event_generic(self, event_generic, args)
        plugin_manager.handle_plugins(self, event_generic, args)
                