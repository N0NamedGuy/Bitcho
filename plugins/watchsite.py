'''
Created on Nov 6, 2011

@author: David
'''
import threading
import urllib2

class SiteWatcher(threading.Thread):
    
    def __init__(self, site, time = 3):
        self.site = site
        self.time = time
        
        print "Watching %s waiting %d seconds" % (site, time)
        
        threading.Thread.__init__(self)
    
    def start(self):
        self.running = True
        threading.Thread.start(self)
    
    def run(self):
        while self.running:
            t = threading.Timer(self.time, self.check)
            t.start()
            t.join()
    
    def stop(self):
        self.running = False
    
    def check(self):
        try:
            response = urllib2.urlopen(self.site)
            html = response.read()
            self.on_refresh(html)
        except Exception, e:
            self.on_error(e)
    
    def on_refresh(self, data):
        pass
    
    def on_eror(self, e):
        pass