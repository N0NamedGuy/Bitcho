'''
Created on Nov 5, 2011

@author: Pedro Borges
'''

from datetime import datetime
from plugin_base import PluginBase

class DatePlugin(PluginBase):
    def plugin_init(self):
        self.register_event("channel_msg", self.on_channel_msg)
        
    def on_channel_msg(self, user, channel, msg):
        if msg.startswith("!date"):
            today = datetime.utcnow().strftime("%H:%M:%S %a %d. %b %Y")
            self.bot.send_msg(channel, today)