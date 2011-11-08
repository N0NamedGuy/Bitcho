import sync_socket
import thread

class LineTooLong(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "message too long"

class IRCUser:
    """Defines an IRC user."""
    nick=None
    username=None
    ip=None
    status=''

    def __init__(self, rawstr):
        """
        Initializes an IRC user.
        
        rawstr - The user description in IRC format
        """
        self.nick=rawstr.split('!')[0]
        self.username=rawstr.split('!')[1].split('@')[0]
        self.ip=rawstr.split('@')[1]

    def __str__(self):
        return str(self.nick)

    def get_nick(self):
        """Returns the user's nick."""
        return self.nick

    def get_user(self):
        """Returns the user's name."""
        return self.username

    def get_ip(self):
        """Returns the user's ip."""
        return self.ip

    def get_status(self):
        """Returns the user's status."""
        return self.status

    def set_status(self, status):
        """Sets the user's status."""
        self.status = status

    def get_nick_wstatus(self):
        """Returns the nick with its user status prepended."""
        return self.status + self.nick

class ircclient:
    """
    A simple IRC client on its own. Every time a message is sent
    from the IRC server, an event is dispatched.
    
    To do a usable IRC client, a class deriving from this one should be done.
    All the necessary event_* methods for the target IRC client (be it a bot,
    an IRC client with an UI, etc) should be implemented.
    """
    # RFC 1459 Numeric Errors 
    RFC_ERR_NOSUCHNICK = 401
    RFC_ERR_NOSUCHSERVER = 402
    RFC_ERR_NOSUCHCHANNEL = 403
    RFC_ERR_CANNOTSENDTOCHAN = 404
    RFC_ERR_TOOMANYCHANNELS = 405
    RFC_ERR_WASNOSUCHNICK = 406
    RFC_ERR_TOOMANYTARGETS = 407
    RFC_ERR_NOORIGIN = 409
    RFC_ERR_NORECIPIENT = 411
    RFC_ERR_NOTEXTTOSEND = 412
    RFC_ERR_NOTOPLEVEL = 413
    RFC_ERR_WILDTOPLEVEL = 414
    RFC_ERR_UNKNOWNCOMMAND = 421
    RFC_ERR_NOMOTD = 422
    RFC_ERR_NOADMININFO = 423
    RFC_ERR_FILEERROR = 424
    RFC_ERR_NONICKNAMEGIVEN = 431
    RFC_ERR_ERRONEUSNICKNAME = 432
    RFC_ERR_NICKNAMEINUSE = 433
    RFC_ERR_NICKCOLLISION = 436
    RFC_ERR_USERNOTINCHANNEL = 441
    RFC_ERR_NOTONCHANNEL = 442
    RFC_ERR_USERONCHANNEL = 443
    RFC_ERR_NOLOGIN = 444
    RFC_ERR_SUMMONDISABLED = 445
    RFC_ERR_USERSDISABLED = 446
    RFC_ERR_NOTREGISTERED = 451
    RFC_ERR_NEEDMOREPARAMS = 461
    RFC_ERR_ALREADYREGISTRED = 462
    RFC_ERR_NOPERMFORHOST = 463
    RFC_ERR_PASSWDMISMATCH = 464
    RFC_ERR_YOUREBANNEDCREEP = 465
    RFC_ERR_KEYSET = 467
    RFC_ERR_CHANNELISFULL = 471
    RFC_ERR_UNKNOWNMODE = 472
    RFC_ERR_INVITEONLYCHAN = 473
    RFC_ERR_BANNEDFROMCHAN = 474
    RFC_ERR_BADCHANNELKEY = 475
    RFC_ERR_NOPRIVILEGES = 481
    RFC_ERR_CHANOPRIVSNEEDED = 482
    RFC_ERR_CANTKILLSERVER = 483
    RFC_ERR_NOOPERHOST = 491
    RFC_ERR_UMODEUNKNOWNFLAG = 501
    RFC_ERR_USERSDONTMATCH = 502

    # RFC 1459 Numeric Replies 
    RFC_RPL_NONE = 300
    RFC_RPL_USERHOST = 302
    RFC_RPL_ISON = 303
    RFC_RPL_AWAY = 301
    RFC_RPL_UNAWAY = 305
    RFC_RPL_NOWAWAY = 306
    RFC_RPL_WHOISUSER = 311
    RFC_RPL_WHOISSERVER = 312
    RFC_RPL_WHOISOPERATOR = 313
    RFC_RPL_WHOISIDLE = 317
    RFC_RPL_ENDOFWHOIS = 318
    RFC_RPL_WHOISCHANNELS = 319
    RFC_RPL_WHOWASUSER = 314
    RFC_RPL_ENDOFWHOWAS = 369
    RFC_RPL_LISTSTART = 321
    RFC_RPL_LIST = 322
    RFC_RPL_LISTEND = 323
    RFC_RPL_CHANNELMODEIS = 324
    RFC_RPL_NOTOPIC = 331
    RFC_RPL_TOPIC = 332
    RFC_RPL_INVITING = 341
    RFC_RPL_SUMMONING = 342
    RFC_RPL_VERSION = 351
    RFC_RPL_WHOREPLY = 352
    RFC_RPL_ENDOFWHO = 315
    RFC_RPL_NAMREPLY = 353
    RFC_RPL_ENDOFNAMES = 366
    RFC_RPL_LINKS = 364
    RFC_RPL_ENDOFLINKS = 365
    RFC_RPL_BANLIST = 367
    RFC_RPL_ENDOFBANLIST = 368
    RFC_RPL_INFO = 371
    RFC_RPL_ENDOFINFO = 374
    RFC_RPL_MOTDSTART = 375
    RFC_RPL_MOTD = 372
    RFC_RPL_ENDOFMOTD = 376
    RFC_RPL_YOUREOPER = 381
    RFC_RPL_REHASHING = 382
    RFC_RPL_TIME = 391
    RFC_RPL_USERSSTART = 392
    RFC_RPL_USERS = 393
    RFC_RPL_ENDOFUSERS = 394
    RFC_RPL_NOUSERS = 395
    RFC_RPL_TRACELINK = 200
    RFC_RPL_TRACECONNECTING = 201
    RFC_RPL_TRACEHANDSHAKE = 202
    RFC_RPL_TRACEUNKNOWN = 203
    RFC_RPL_TRACEOPERATOR = 204
    RFC_RPL_TRACEUSER = 205
    RFC_RPL_TRACESERVER = 206
    RFC_RPL_TRACENEWTYPE = 208
    RFC_RPL_TRACELOG = 261
    RFC_RPL_STATSLINKINFO = 211
    RFC_RPL_STATSCOMMANDS = 212
    RFC_RPL_STATSCLINE = 213
    RFC_RPL_STATSNLINE = 214
    RFC_RPL_STATSILINE = 215
    RFC_RPL_STATSKLINE = 216
    RFC_RPL_STATSYLINE = 218
    RFC_RPL_ENDOFSTATS = 219
    RFC_RPL_STATSLLINE = 241
    RFC_RPL_STATSUPTIME = 242
    RFC_RPL_STATSOLINE = 243
    RFC_RPL_STATSHLINE = 244
    RFC_RPL_UMODEIS = 221
    RFC_RPL_LUSERCLIENT = 251
    RFC_RPL_LUSEROP = 252
    RFC_RPL_LUSERUNKNOWN = 253
    RFC_RPL_LUSERCHANNELS = 254
    RFC_RPL_LUSERME = 255
    RFC_RPL_ADMINME = 256
    RFC_RPL_ADMINLOC1 = 257
    RFC_RPL_ADMINLOC2 = 258
    RFC_RPL_ADMINEMAIL = 259

    # RFC 2812 Numeric replies
    RFC_RPL_WELCOME = 001
    RFC_RPL_YOURHOST = 002
    RFC_RPL_CREATED = 003
    RFC_RPL_MYINFO = 004
    RFC_RPL_BOUNCE = 005

    # RFC 2812 Reserved numerics
    RFC_RPL_SERVICEINFO = 231
    RFC_RPL_ENDOFSERVICES = 232
    RFC_RPL_SERVICE = 233
    RFC_RPL_NONE = 300
    RFC_RPL_WHOISCHANOP = 316
    RFC_RPL_KILLDONE = 361
    RFC_RPL_CLOSING = 362
    RFC_RPL_CLOSEEND = 363
    RFC_RPL_INFOSTART = 373
    RFC_RPL_MYPORTIS = 384
    RFC_RPL_STATSCLINE = 213
    RFC_RPL_STATSNLINE = 214
    RFC_RPL_STATSILINE = 215
    RFC_RPL_STATSKLINE = 216
    RFC_RPL_STATSQLINE = 217
    RFC_RPL_STATSYLINE = 218
    RFC_RPL_STATSVLINE = 240
    RFC_RPL_STATSLLINE = 241
    RFC_RPL_STATSHLINE = 244
    RFC_RPL_STATSSLINE = 244
    RFC_RPL_STATSPING = 246
    RFC_RPL_STATSBLINE = 247
    RFC_RPL_STATSDLINE = 250
    RFC_ERR_NOSERVICEHOST = 492

    # mIRC Colors
    MIRC_COLOR_RESET = chr(0x0F)
    MIRC_COLOR_BOLD = chr(0x02)
    MIRC_COLOR_UNDERLINE = chr(0x1F)
    MIRC_COLOR = chr(0x03)
    MIRC_COLORS = {}
    MIRC_COLORS['white'] = str(0)
    MIRC_COLORS['black'] = str(1)
    MIRC_COLORS['blue'] = str(2)
    MIRC_COLORS['green'] = str(3)
    MIRC_COLORS['red'] = str(4)
    MIRC_COLORS['brown'] = str(5)
    MIRC_COLORS['purple'] = str(6)
    MIRC_COLORS['orange'] = str(7)
    MIRC_COLORS['yellow'] = str(8)
    MIRC_COLORS['light_green'] = str(9)
    MIRC_COLORS['teal'] = str(10)
    MIRC_COLORS['light_cyan'] = str(11)
    MIRC_COLORS['light_blue'] = str(12)
    MIRC_COLORS['pink'] = str(13)
    MIRC_COLORS['grey'] = str(14)
    MIRC_COLORS['silver'] = str(15)

    MSG_MAX_LENGTH=3*1024 # 3KB

    nick=None 
    host=None
    port=None
    s=None
    running=False # am I still running?

    state='' # am I waiting for some data from server?
    channels={}

    DEBUG=False

    def __init__(self, host, port):
        """
        Makes a connection to an IRC server.
        
        host - the IRC server's host
        port - the IRC server's listening port
        """
        self.host=host
        self.port=port
        self.s=sync_socket.SyncronizedSocket()
        self.s.setblocking(1)

    def get_nick(self):
        """
        Returns the client's nick.
        """
        return self.nick

    def get_host(self):
        """
        Returns the IRC server host.
        """
        return self.host

    def get_port(self):
        """
        Returns the IRC server listening port.
        """
        return self.port
    
    def connect(self):
        """
        Connects to the IRC server.
        """
        self.s.connect((self.host,self.port))
        self.s.settimeout(1) # timeout for blocking operations in seconds

    def close(self):
        """
        Closes the connection to the IRC server.
        """
        if self.DEBUG:
            print 'Closing client'
        self.running = False
        self.s.close()

    def nick(self, nick):
        """
        Change the client's nick.
        """
        self.send('NICK '+nick)
        self.nick=nick

    def send(self, msg):
        """
        Sends a command to the IRC server. Refer to the IRC
        RFCs for the command syntax.
        """
        if len(msg)+2 > self.MSG_MAX_LENGTH:
            raise LineTooLong

        while True:
            try:
                self.s.send(msg+'\r\n')
                if self.DEBUG:
                    print "<<" + msg
            except sync_socket.socket.timeout:
                self.periodic_run()
                continue
            break

    def send_msg(self, dest, msg):
        """
        Sends a message to a user or channel.
        
        dest - Can be either a channel or a nick
        msg - The message to be delivered
        """
        self.send('PRIVMSG '+dest+' :'+msg)

    def send_msg_color(self, chan, msg):
        """
        Sends a message to a user or channel, with a special syntax.
        Refer to doc/COLOURS.txt for more info on the colour syntax.
        
        dest - Can be either a channel or a nick
        msg - The message to be delivered
        """
        msg_tokens = msg.split(' ')
        new_msg=''
        print_space = True 
        first=True

        for token in msg_tokens:
            if '%' in token:
                if token == '%normal':
                    new_msg += self.MIRC_COLOR_RESET
                    print_space = False 
                    continue
                elif token == '%bold':
                    new_msg += self.MIRC_COLOR_BOLD
                    print_space = False
                    continue
                elif token == '%underline':
                    new_msg += self.MIRC_COLOR_UNDERLINE
                    print_space = False
                    continue
                else:
                    colors = token.split('%') # fg%bg
                    color=''
                    if len(colors) == 2 and colors[1] in self.MIRC_COLORS:
                        color = self.MIRC_COLOR + self.MIRC_COLORS[colors[1]]
                        if colors[0] in self.MIRC_COLORS:
                            color += ',' + self.MIRC_COLORS[colors[0]]
                        new_msg += color
                        print_space = False
                        continue
                         
                if new_msg != '':
                    new_msg += (' ' if print_space else '') + token.replace('%%','%') 
                    print_space = True
                else:
                    new_msg += token.replace('%%','%') 
                    
            else:
                new_msg += (' ' if print_space and not first else '') + token
                print_space = True

            first=False

        self.send_msg(chan, new_msg)

    def names(self, chan):
        """
        Sends a NAMES command to the IRC server.
        
        chan - The channel to query
        """
        self.send('NAMES '+chan)

    def who(self, chan):
        """
        Sends a WHO command to the IRC server.
        
        chan - The channel to query
        """
        self.send('WHO '+chan)

    def get_users(self, chan):
        """
        Returns an array containing all the users in the specified channel.
        
        chan - The channel
        """
        return self.channels[chan] if chan in self.channels else None

    def get_user_status(self, chan, nick):
        """
        Gets a user status (op, voice, none) in a specified channel.
        
        chan - The channel
        nick - The user's nick
        """
        return self.channels[chan][nick].get_status()\
            if chan in self.channels and nick in self.channels[chan] else None
    
    def get_channels(self):
        """
        Returns the channels where the client has joined.
        """
        return self.channels.keys()
    
    def join(self, chan):
        """
        Joins a channel.
        
        chan - The channel to join.
        """
        self.send('JOIN '+chan)    
        self.who(chan) 
    
    def quit(self, msg): #@ReservedAssignment
        """
        Sends a quit message to the IRC server.
        
        msg - Quit message
        """
        self.send('QUIT '+msg)

    def send_all(self, msgs):
        """
        Sends mutiple commands to the IRC server.
        
        msgs - An array containing the messages
        """
        for msg in msgs:
            self.send(msg)

    def part(self, chan, reason=''):
        """
        Leave (or part) a channel.
        
        chan - The channel to leave
        reason - An optional message explaining the leave
        """
        self.send('PART '+chan+' :'+reason) 
        if chan in self.channels:
            del self.channels[chan]

    def periodic_run(self):
        """
        This method is called when the socket times out.
        Subclasses may use this method for periodic checks.
        """
        pass

    def recv_loop(self):
        """
        Runs the client, by starting the event loop. This method is a blocking one.
        """
        buf=''

        self.running = True
        while self.running:
            try:
                buf+=self.s.recv(1024*32)
                if buf == '': # TCP Connection went down :(
                    self.running = False
                    self.event_socket_closed()
                    return

            except sync_socket.socket.timeout:
                self.periodic_run()
                continue

            while buf.find('\r\n') >= 0:
                e=buf.find('\r\n')
                line=buf[0:e]
                buf=buf[e+2:]
                
                if self.DEBUG:
                    print '>>' + line

                tokens=line.split(' ')
                if len(tokens) > 0:
                    self.__handle_event(tokens,line)

        self.close()

    def __handle_event(self, tokens, raw):
        event = None
        args = []
        
        if len(tokens) >= 3 and tokens[1].isdigit():
            numparams = []
            for token in tokens[3:]:
                if token[0] != ':':
                    numparams.append(token)
                else:
                    break

            self.event_numeric(int(tokens[1]), \
                tokens[2],\
                numparams,\
                raw[raw.find(':',1)+1:])

        elif len(tokens) == 2 and tokens[0].lower() == 'ping':
            event = 'ping'
            args = [tokens[1][1:]]
            
            self.event_ping(*args)
        
        elif len(tokens) >= 4 and tokens[1].lower() == 'privmsg':
            if tokens[2][0] == '#':
                event = 'channel_msg'
                args = [IRCUser(tokens[0][1:]),tokens[2],
                                       raw[raw.find(':',1)+1:]]
            
                self.event_channel_msg(*args)
            else:
                event = 'priv_msg'
                args = [IRCUser(tokens[0][1:]),
                                    raw[raw.find(':',1)+1:]]
                
                self.event_priv_msg(*args)
                
        elif len(tokens) >= 4 and tokens[1].lower() == 'notice':
            if tokens[2][0] == '#':
                event = 'channel_notice'
                args = [IRCUser(tokens[0][1:]),tokens[2],
                                       raw[raw.find(':',1)+1:]]
            
                self.event_channel_notice(*args)
            else:
                event = 'priv_notice'
                args = [IRCUser(tokens[0][1:]),
                                    raw[raw.find(':',1)+1:]]
                
                self.event_priv_notice(IRCUser(tokens[0][1:]),
                                    raw[raw.find(':',1)+1:])
        
        elif len(tokens) >= 5 and tokens[1].lower() == 'kick':
            event = 'kick'
            args = [IRCUser(tokens[0][1:]),tokens[3],
                                tokens[2],raw[raw.find(':',1)+1:]]
            
            self.event_kick(*args)
        
        elif len(tokens) == 3 and tokens[1].lower() == 'nick':
            new_nick=tokens[2][1:]
            
            event = 'nick'
            args = [IRCUser(tokens[0][1:]), new_nick]
             
            if self.nick == IRCUser(tokens[0][1:]).get_nick():
                self.nick=new_nick

            self.event_nick(*args)

        elif len(tokens) >= 5 and tokens[1].lower() == 'mode':
            args = [IRCUser(tokens[0][1:]),tokens[2], tokens[4]]
           
            if tokens[3] == '+o':
                event = 'op'
                self.event_op(*args)
            elif tokens[3] == '-o':
                event = 'deop'
                self.event_deop(*args)
            elif tokens[3] == '+v':
                event = 'voice'
                self.event_voice(*args)
            elif tokens[3] == '-v':
                event = 'devoice'
                self.event_devoice(*args)
            else:
                event = 'mode'
                args = [IRCUser(tokens[0][1:]),tokens[2],tokens[3], tokens[4]]
        
        elif len(tokens) >= 3 and tokens[1].lower() == 'part':
            event = 'part'
            args = [IRCUser(tokens[0][1:]), tokens[2], raw[raw.find(':',1)+1:]]
            self.event_part(*args)
                     
        elif len(tokens) >= 3 and tokens[1].lower() == 'join':
            event = 'join'
            args = [IRCUser(tokens[0][1:]), tokens[2][1:]]
            self.event_join(*args)
    
        elif len(tokens) >= 2 and tokens[1].lower() == 'kill':
            event = 'kill'
            args = [IRCUser(tokens[0][1:]), raw[raw.find(':',1)+1:]]
            self.event_kill(*args)
    
        elif len(tokens) >= 2 and tokens[1].lower() == 'quit':
            event = 'quit'
            args = [IRCUser(tokens[0][1:]), raw[raw.find(':',1)+1:]]
            self.event_quit(*args)
        
        elif len(tokens) >= 2:
            event = tokens[1].lower()
            args = tokens
        
        self.event_raw(tokens, raw);
        if event != None:
            self.event_non_numeric(event, args)
    
    def event_raw(self, tokens, raw):
        """
        This method is called when the IRC server sends any message.
        
        tokens - An array containing all the tokens
        raw - The line sent by the IRC server without the trailing \r\n
        """
        pass
    
    def event_ping(self, msg):
        """
        This method is called when the IRC server sends a PING message.
        
        msg - The msg the client should return to the server in a PONG message
        """
        self.send('PONG :'+msg)

    def event_op(self, user, channel, nick_oped):
        """
        This method is called when an user is given operator status.
        
        user - A ircclient.IRCUser object specifying the user who gave
            operator status
        channel - The channel where such status was granted
        nick_oped - The lucky basterd who is now an operator
        """
        
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' oped '+nick_oped \
                +' in '+channel
        
        self.who(channel)

    def event_deop(self, user, channel, nick_oped):
        """
        This method is called when an user loses his operator status.

        user - A ircclient.IRCUser object specifying the user who took away
            operator status
        channel - The channel where such status was revoked
        nick_oped - The poor guy who is now a commoner
        """
        
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' deoped '+nick_oped \
                +' in '+channel
        
        # The user is not op anymore, but it can be voice
        # so, we run a who query to update his situation
        self.who(channel)
        #self.channels[channel][nick_oped].set_status('')

    def event_voice(self, user, channel, nick_oped):
        """
        This method is called when an user is given voice status.
        
        user - A ircclient.IRCUser object specifying the user who gave
            voice status
        channel - The channel where such status was granted
        nick_oped - The voiced user
        """
        
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' voiced '+nick_oped \
                +' in '+channel

        # Because i feel lazy, i just run a who...
        self.who(channel)

    def event_devoice(self, user, channel, nick_oped):
        """
        This method is called when an user loses voice status.
        
        user - A ircclient.IRCUser object specifying the user who gave
            voice status
        channel - The channel where such status was revoked
        nick_oped - The devoiced user
        """
        
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' devoiced '+nick_oped \
                +' in '+channel
                            
        # The user is not voice anymore, but he can be still op
        # so, we run a who query to update his situation
        self.who(channel)
        #self.channels[channel][nick_oped].set_status('')

    def event_channel_msg(self, user, channel, msg):
        """
        This method is called when an user sends a message to a channel.
        
        user - A ircclient.IRCUser object specifying the user who sent the
            message
        channel - A string representing the channel to where the message was
            sent
        msg - The message itself
        """
        
        if self.DEBUG:
            print 'DEBUG channel msg @ '+channel+' by '+(user.get_nick()) \
                +': '+msg
                
    def event_channel_notice(self, user, channel, notice):
        """
        This method is called when an user sends a notice to a channel.
        
        user - A ircclient.IRCUser object specifying the user who sent the
            notice
        channel - A string representing the channel to where the message was
            sent
        notice - The notice itself
        """
        if self.DEBUG:
            print 'DEBUG notice msg @ '+channel+' by '+(user.get_nick()) \
                +': '+notice

    def event_join(self, user, channel):
        """
        This method is called when an user joins a channel.
        
        user - A ircclient.IRCUser object specifying the user who joined the
            channel
        channel - A string representing the joined channel
        """
        if self.DEBUG:
            print 'DEBUG ' + (user.get_nick()) + ' joined channel ' \
                + channel

        if channel in self.channels and not (user.get_nick() in self.channels[channel]):
            self.channels[channel][user.get_nick()] = user
        
        elif not channel in self.channels:
            self.channels[channel] = {}

        # To be on the safe side, we run WHO to update anything we missed
        # namely, the user's status
        self.who(channel)
        if self.DEBUG:
            print self.channels[channel]
    
    def event_part(self, user, channel, msg):
        """
        This method is called when an user leaves (or parts) a channel.
        
        user - A ircclient.IRCUser object specifying the user who left the
            channel
        channel - A string representing the channel the user left
        msg - A part message
        """        
        
        if self.DEBUG:
            print 'DEBUG ' + (user.get_nick()) + ' left channel ' \
                + channel + '. reason: "' + msg + '"'

        if not(channel in self.channels):
            return
        
        if self.get_nick() == user.get_nick():
            del self.channels[channel]
        elif user.get_nick() in self.channels[channel]:
            del self.channels[channel][user.get_nick()]
        
            if self.DEBUG:
                print self.channels[channel]

    def event_priv_msg(self, user, msg):
        """
        This method is called when an user sends a message directly to the
        client.
        
        user - A ircclient.IRCUser object specifying the user who sent the
            message
        msg - The sent message
        """
        if self.DEBUG:
            print 'DEBUG priv msg by '+(user.get_nick())+': '+msg
            
    def event_priv_notice(self, user, notice):
        """
        This method is called when an user sends a notice directly to the
        client.
        
        user - A ircclient.IRCUser object specifying the user who sent the
            notice
        notice - The sent notice
        """
        if self.DEBUG:
            print 'DEBUG notice msg by '+(user.get_nick())+': '+notice

    def event_kick(self, user, kicked_nick, chan, reason):
        """
        This method is called when an user is kicked from a channel.
        
        user - A ircclient.IRCUser object specifying the user who kicked
        kicked_nick - The poor basterd nick's that got kicked out
        chan - The channel from where there was a kick
        reason - The kick reason
        """
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' kicked '+kicked_nick \
                +' from '+chan+' msg: '+reason

        if (kicked_nick == self.get_nick()):
            if self.DEBUG:
                print 'I GOT KICKED :('
            del self.channels[chan]
        else:
            if self.DEBUG:
                print self.channels[chan]
            del self.channels[chan][kicked_nick]
            if self.DEBUG:
                print self.channels[chan]
    
    def event_nick(self, user, new_nick):
        """
        This method is called when an user changes nick.
        
        user - A ircclient.IRCUser object specifying the user who changed the
            nick
        new_nick - The new nickname
        """
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' changed nick to '+new_nick
        
        # FIXME: This can be done without resorting to /WHO
        for chan in self.channels.keys():
            self.who(chan)


    def event_quit(self, user, reason):
        """
        This method is called when an user quits the IRC server.
        
        user - A ircclient.IRCUser object specifying the user who quitted
        reason - The quit reason
        """
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' has quit. Reason: ' + \
                reason
 
        # FIXME: This can be done without resorting to /WHO
        for chan in self.channels.keys():
            self.who(chan)

    def event_kill(self, user, reason):
        """
        This method is called when an user gets "killed" by an IRC operator.
        
        user - A ircclient.IRCUser object specifying the user who got killed
        reason - The kill reason
        """
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' got killed! Reason: ' + \
                reason

    def make_raw_nick(self, nick, user, host):
        """
        Returns an assembled IRC nick.
        """
        return nick + '!' + user + '@' + host

    def event_numeric(self, event_num, nick, params, msg):
        """
        This method is called whenever a numeric reply gets received by the
        client. See the IRC RFC for more details on the parameters.
        
        event_num - The event number
        nick - The nick who sent triggered the reply
        params - The reply parameters
        msg - The reply message 
        """
        if event_num == self.RFC_RPL_NAMREPLY:
            if self.DEBUG:
                chan = params[len(params) - 1]
                print 'DEBUG Users in ' + chan + ': ' + msg

        elif event_num == self.RFC_RPL_WHOREPLY:
            chan = params[0]
            username = params[1]
            host = params[2]
            nickname = params[4]

            # FIXME: This is ugly!
            if len(params[5]) == 2:
                status = params[5][1]
            else:
                status = ''

            if self.state == '':
                self.state = 'WHO'
                self.channels[chan] = {}

            self.channels[chan][nickname] = IRCUser(self.make_raw_nick(nickname, username, host))
            self.channels[chan][nickname].set_status(status)

        elif event_num == self.RFC_RPL_ENDOFWHO:
            self.state = ''
    
    def event_non_numeric(self, event, args):
        """
        This method is called when the IRC server sends a non numeric message.
        
        event - A string describing the event
        args - An array with the parameters to the event
        """
        pass
    
    def event_socket_closed(self):
        """
        This method is called when the connection is closed or lost.
        """
        if self.DEBUG:
            print 'DEBUG socket closed'

