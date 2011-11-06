'''
Created on Nov 6, 2011

@author: David
'''
import json
from plugin_base import PluginBase
from plugins.watchsite import SiteWatcher

class StreamWatcher(SiteWatcher):
    def __init__(self, bot, stream):
        self.stream = stream
        self.bot = bot
        
        SiteWatcher.__init__(self, "http://%s/7.html" % (stream["ip"],) , int(stream["refresh"]))
        self.status = None
        self.check()
        
    def on_error(self, e):
        if (self.status):
            notify = self.stream["notify"]
            for n in notify:
                self.bot.send_msg(n, "'%s' in now down..." %
                              (self.stream["name"],))
            
        self.status = False

    def on_refresh(self, data):
        if (self.status == False):
            notify = self.stream["notify"]
            for n in notify:
                self.bot.send_msg(n, "'%s' in now up! Listen to it at %s" %
                              (self.stream["name"], self.stream["stream"]))
            
        self.status = True

class FreeStreamHostingPlugin(PluginBase):
    def plugin_init(self):
        self.register_event("connect", self.on_connect)
        
    def on_connect(self):
        try:
            f = open("plugins/conf/freestreamhosting.json")
            conf = json.load(f)["streams"]
            f.close()
        except Exception, e:
            print e
            return
        
        self.streams = []
        for stream in conf:
            watcher = StreamWatcher(self.bot, stream)
            watcher.start()
            self.streams.append(watcher)
            