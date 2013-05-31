'''
Created on May 31, 2013

@author: David Serrano
'''
import json
import re
import urllib2
from plugins.lib.BeautifulSoup.BeautifulSoup import BeautifulSoup
from plugin_base import PluginBase

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# Lower permissions have higher precedence
class UrlPlugin(PluginBase):
    
    def parse_url(self, url, dest):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(url)

        html = response.read()
        soup = BeautifulSoup(html)
        title = soup.findAll("title")

        if len(title) > 0:
            title_str = title[0].string
            self.bot.send_msg(dest, title_str)

    def plugin_init(self):
        self.register_event("channel_msg", self.on_channel_msg)

    def on_channel_msg(self, user, channel, msg):
        urls = re.findall(url_regex, msg)

        for url in urls:
            self.parse_url(url, channel)
