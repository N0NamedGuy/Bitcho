'''
Created on Nov 2, 2011

@author: David
'''
import threading

# code from
# http://softwareramblings.com/2008/06/running-functions-as-threads-in-python.html
class FunThread(threading.Thread):
    """
    Runs a function in its own thread
    """
    
    def __init__(self, target, args = []):
        """
        Initializes the thread.
        
        target - a function pointer
        args - an array containing arguments to be passed
            to the target function
        """
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        """
        @see: threading.Thread.run
        """
        self._target(*self._args)