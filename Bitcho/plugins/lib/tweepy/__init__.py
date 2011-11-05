# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

"""
Tweepy Twitter API library
"""
__version__ = '1.8'
__author__ = 'Joshua Roesslein'
__license__ = 'MIT'

from plugins.lib.tweepy.models import Status, User, DirectMessage, Friendship, SavedSearch, SearchResult, ModelFactory
from plugins.lib.tweepy.error import TweepError
from plugins.lib.tweepy.api import API
from plugins.lib.tweepy.cache import Cache, MemoryCache, FileCache
from plugins.lib.tweepy.auth import BasicAuthHandler, OAuthHandler
from plugins.lib.tweepy.streaming import Stream, StreamListener
from plugins.lib.tweepy.cursor import Cursor

# Global, unauthenticated instance of API
api = API()

def debug(enable=True, level=1):

    import httplib
    httplib.HTTPConnection.debuglevel = level

