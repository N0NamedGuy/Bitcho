'''
Created on Nov 8, 2011

@author: Pedro Borges
@author: David Serrano
'''
import threading
import socket

class SyncronizedSocket(socket.socket):
    def __init__(self, *args, **kwargs):
        socket.socket.__init__(self, *args, **kwargs)
        self.socket_lock = threading.Lock()

    def send(self, string, *flags):
        with self.socket_lock:
            self.socket.send(string, *flags)

    def recv(self, bufsize, *flags):
        with self.socket_lock:
            return self.socket.recv(bufsize, *flags)

    def __enter__(self):
        return self
        
    def __exit__(self, *args):
        self.close()