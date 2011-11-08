#!/usr/bin/env python2.7
import json
import httplib
import urllib
import xml.dom.minidom
import re,htmlentitydefs
from plugin_base import PluginBase

broadcast = True 
def unescape(text):
    """Removes HTML or XML character references 
    and entities from a text string.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
        # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        
        return text # leave as is
        
    return re.sub("&#?\w+;", fixup, text)

def make_web_req(server, req):
    h = httplib.HTTPConnection(server)
    h.request('GET', req)
    r = h.getresponse()
    rep = r.read()
    #print rep
    return rep

def get_xml_doc(server, req):
    return xml.dom.minidom.parseString(make_web_req(server,req))

def get_child_node(parentNode, childName):
    for node in parentNode.childNodes:
        if node.nodeName.lower() == childName.lower():
            return node

    return None

def strip_sgml_tags(string):
    p = re.compile(r'<.*?>')
    return p.sub('', string)

class lastfm:
    apikey=''
    mirror = 'ws.audioscrobbler.com'
    user_dict = {} 

    max_similar_artists = 5
    max_tasteometer = 5

    def __init__(self):
        try:
            f = open("plugins/conf/lastfm.json",'r')
            self.conf = json.load(f)
            f.close()
        
            self.user_dict = self.conf['userlist']
            self.apikey = self.conf['apikey']
        except Exception:
            pass

    def get_lastfm_user(self, username):
        try:
            return self.user_dict[username]
        except:
            return username

    def search_artist(self, artist):
        req = '/2.0/?method=artist.search&artist=%s&limit=1&api_key=%s' % (urllib.quote(artist), self.apikey)
        doc = get_xml_doc(self.mirror, req)
      
        lfmNode = get_child_node(doc, 'lfm')
        resultsNode = get_child_node(lfmNode, 'results')         
        matchesNode = get_child_node(resultsNode, 'artistmatches')
        
        if len(matchesNode.childNodes) == 0:
            return None
        
        artistNode = get_child_node(matchesNode, 'artist')
        if artistNode != None:
            nameNode = get_child_node(artistNode, 'name')
            return nameNode.childNodes[0].nodeValue
        else:
            return None

    def get_artist_info(self, artist):
        
        artist = self.search_artist(artist)
        if artist == None:
            return 'No info was found for this artist' 
        
        req = '/2.0/artist/' + urllib.quote(artist)  + '/info.xml'
        doc = get_xml_doc(self.mirror, req)

        artistNode = get_child_node(doc, 'artist')
        nameNode = get_child_node(artistNode, 'name')
        bioNode = get_child_node(artistNode, 'bio')
        summaryNode = get_child_node(bioNode, 'summary')

        name = nameNode.childNodes[0].nodeValue
        if len(summaryNode.childNodes) > 0:
            summary = summaryNode.childNodes[0].nodeValue
        else:
            summary = 'No summary was found for this artist.'
        return '* %s *\n%s' % (name, unescape(strip_sgml_tags(summary)))

    def get_artist_similar(self, artist):
        
        artist = self.search_artist(artist)
        if artist == None:
            return 'No info was found for this artist' 

        req = '/2.0/?method=artist.getsimilar&artist=%s&api_key=%s&limit=%d' \
            % (urllib.quote(artist), self.apikey, self.max_similar_artists)
        doc = get_xml_doc(self.mirror, req)

        lfmNode = get_child_node(doc, 'lfm')
        similarNode = get_child_node(lfmNode, 'similarartists')

        artists = []
        for node in similarNode.childNodes:
            if node.nodeName == 'artist':
                nameNode = get_child_node(node, 'name')
                artists.append(nameNode.childNodes[0].nodeValue)

        return 'Similar artists to: %s\n* %s' % (artist, '\n* '.join(artists))

    def get_tasteometer_user(self, user1, user2):
       
        user1 = self.get_lastfm_user(user1)
        user2 = self.get_lastfm_user(user2)
        
        req = '/2.0/?method=tasteometer.compare&type1=user&type2=user&value1=%s&value2=%s&api_key=%s&limit=%d' \
            % (urllib.quote(user1), urllib.quote(user2), self.apikey, self.max_tasteometer)

        doc = get_xml_doc(self.mirror, req)
        lfmNode = get_child_node(doc, 'lfm')

        if lfmNode.getAttribute('status') == 'failed':
            errorNode = get_child_node(lfmNode, 'error')
            return errorNode.childNodes[0].nodeValue

        comparisonNode = get_child_node(lfmNode, 'comparison')
        resultNode = get_child_node(comparisonNode, 'result')

        scoreNode = get_child_node(resultNode, 'score')
        score = float(scoreNode.childNodes[0].nodeValue)

        return 'Musical compatibility score: %d%% [%s - %s]'\
             % (int(score * 100), user1, user2)

    def get_last_played(self, user):
        user = self.get_lastfm_user(user)
        
        req = '/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&limit=1' \
            % (urllib.quote(user), self.apikey)

        doc = get_xml_doc(self.mirror, req)
        lfmNode = get_child_node(doc, 'lfm')
        
        if lfmNode.getAttribute('status') == 'failed':
            errorNode = get_child_node(lfmNode, 'error')
            return errorNode.childNodes[0].nodeValue

        recentNode = get_child_node(lfmNode, 'recenttracks')
        trackNode = get_child_node(recentNode, 'track')

        if trackNode == None:
            return 'The user %s hasn\'t played anything yet' % (user,)

        nowPlaying = trackNode.getAttribute('nowplaying') == 'true'
        
        music = ''
        artist = ''
        album = ''
        for node in trackNode.childNodes:
            if node.hasChildNodes():
                if node.nodeName == 'name': music = node.childNodes[0].nodeValue
                if node.nodeName == 'artist': artist = node.childNodes[0].nodeValue
                if node.nodeName == 'album': album = node.childNodes[0].nodeValue

        outmsg = '%s is now playing: ' % (user,) if nowPlaying else '%s last played: ' % (user,)
        if music != '':
            outmsg += music

        if artist != '':
            outmsg += ' - ' + artist

        if album != '':
            outmsg += ' (' + album + ')'

        return outmsg.encode('utf-8')


class LastFmPlugin(PluginBase):
    def plugin_init(self):
        self.register_event("cmd_lastfm", self.on_command)
        self.lfm = lastfm()
        
    def on_command(self, user, channel, cmd, args):
        if cmd != "lastfm":
            return
        
        if len(args) == 0:
            self.bot.send_notice('Please input a command. ' +
                'Available commands: artist, similar, taste or playing.')
            return
        
        lcmd = args[0]
        largs = args[1:]
        
        if channel != "":
            target = channel
        else:
            target = user.get_nick()
        
        if lcmd == 'artist' and len(largs) >= 1:
            lines = self.lfm.get_artist_info(' '.join(largs[0:]))
            for line in lines.splitlines():
                self.bot.send_notice(user.get_nick(), line)
        elif lcmd == 'similar' and len(largs) >= 1:
            lines = self.lfm.get_artist_similar(' '.join(largs[0:]))
            for line in lines.splitlines():
                self.bot.send_notice(user.get_nick(), line)
        elif lcmd == 'taste' and len(largs) == 2:
            self.bot.send_msg(target, self.lfm.get_tasteometer_user(largs[0], largs[1]))
        elif (lcmd == 'playing') and len(args) == 1:
            self.bot.send_msg(target, self.lfm.get_last_played(largs[0]))
        elif len(largs) == 0:
            self.bot.send_msg(target, self.lfm.get_last_played(lcmd))
        else:
            self.bot.send_notice(user.get_nick(), 'Invalid command! ' +
                'Available commands: artist, similar, taste or playing.')
