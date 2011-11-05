'''
Created on Nov 2, 2011

@author: David Serrano
'''
import json
import sys

from plugin_base import PluginBase
from plugins.lib import tweepy

class TwitterListener(tweepy.StreamListener):
    def __init__(self, bot, out_chan):
        tweepy.StreamListener.__init__(self)
        self.bot = bot
    
    def on_status(self, status):
        try:
            msg = "<@%s> - %s" % (status.author.screen_name, status.text)
            # TODO: Change this
            self.bot.send_msg("out_chan", msg)
            
        except Exception:
            pass
        
        return tweepy.StreamListener.on_status(self, status)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


class TwitterPlugin(PluginBase):
    
    def plugin_init(self):
        self.register_event("connect", self.on_connect)
    
    def on_connect(self):
        fp = open("plugins/conf/twitter.json")
        conf = json.load(fp)
        fp.close()
        
        auth = tweepy.BasicAuthHandler(conf['user'], conf['password'])
        conf['password'] = None
        
        self.listener = TwitterListener(self.bot)
        
        api = tweepy.API()
        #TODO: Change this
        user = api.get_user("n0namedguy")
        
        self.stream = tweepy.Stream(auth, self.listener)
        self.stream.filter(follow = [user.id_str])
