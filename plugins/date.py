'''
Created on Nov 5, 2011

@author: Pedro Borges
@author: David Serrano
'''

from datetime import datetime
from plugin_base import PluginBase

class DatePlugin(PluginBase):
    def plugin_init(self):
        self.register_event("cmd_date", self.on_command)
        
    def on_command(self, user, channel, cmd, args):
        today = datetime.utcnow().strftime("%H:%M:%S %a %d. %b %Y")
        self.bot.send_msg(channel, today)