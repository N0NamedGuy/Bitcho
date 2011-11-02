'''
Created on Nov 2, 2011

@author: David
'''
import threading

# code from
# http://softwareramblings.com/2008/06/running-functions-as-threads-in-python.html
class FunThread(threading.Thread):
    def __init__(self, target, args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)