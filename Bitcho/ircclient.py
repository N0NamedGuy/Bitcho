import socket
import thread

class LineTooLong(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "message too long"

class irc_user:
    nick=None
    username=None
    ip=None
    status=''

    def __init__(self, rawstr):
        self.nick=rawstr.split('!')[0]
        self.username=rawstr.split('!')[1].split('@')[0]
        self.ip=rawstr.split('@')[1]

    def __str__(self):
        return str(self.nick)

    def get_nick(self):
        return self.nick

    def get_user(self):
        return self.username

    def get_ip(self):
        return self.ip

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_nick_wstatus(self):
        return self.status + self.nick

class ircclient:
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
    lock=None # mutex for multithreading
    running=False # am I still running?

    state='' # am I waiting for some data from server?
    channels={}

    DEBUG=True

    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.s=socket.socket()
        self.s.setblocking(1)
        self.lock=thread.allocate_lock()

    def get_nick(self):
        return self.nick

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port
    
    def connect(self):
        self.s.connect((self.host,self.port))
        self.s.settimeout(1) # timeout for blocking operations in seconds

    def close(self):
        print 'Closing bot'
        self.running = False
        self.s.close()

    def nick(self, nick):
        self.send('NICK '+nick)
        self.nick=nick

    def send(self, msg):
        if len(msg)+2 > self.MSG_MAX_LENGTH:
            raise LineTooLong

        while True:
            try:
                self.lock.acquire()
                self.s.send(msg+'\r\n')
                self.lock.release()
                if self.DEBUG:
                    print "<<" + msg
            except socket.timeout:
                self.lock.release()
                self.periodic_run()
                continue
            break

    def send_msg(self, dest, msg):
        self.send('PRIVMSG '+dest+' :'+msg)

    def send_msg_color(self, chan, msg):
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
        self.send('NAMES '+chan)

    def who(self, chan):
        self.send('WHO '+chan)

    def get_users(self, chan):
        return self.channels[chan] if chan in self.channels else None

    def get_user_status(self, chan, nick):
        return self.channels[chan][nick].get_status()\
            if chan in self.channels and nick in self.channels[chan] else None
    
    def get_channels(self):
        return self.channels.keys()
    
    def join(self, chan):
        self.send('JOIN '+chan)    
        self.who(chan) 
    
    def quit(self, msg):
        self.send('QUIT '+msg)

    def send_all(self, msgs):
        for msg in msgs:
            self.send(msg)

    def part(self, chan, reason):
        self.send('PART '+chan+' :'+reason) 
        if chan in self.channels:
            del self.channels[chan]

    def periodic_run(self):
        pass

    def recv_loop(self):
        buffer=''

        self.running = True
        while self.running:
            try:
                buffer+=self.s.recv(1024*32)
                if buffer == '': # TCP Connection went down :(
                    self.running = False
                    self.event_socket_closed()
                    return

            except socket.timeout:
                self.periodic_run()
                continue

            while buffer.find('\r\n') >= 0:
                e=buffer.find('\r\n')
                line=buffer[0:e]
                buffer=buffer[e+2:]
                
                if self.DEBUG:
                    print '>>' + line

                tokens=line.split(' ')
                if len(tokens) > 0:
                    self.handle_event(tokens,line)

        self.close()

    def handle_event(self, tokens, raw):
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
            self.event_ping(tokens[1][1:])
        
        elif len(tokens) >= 4 and tokens[1].lower() == 'privmsg':
            if tokens[2][0] == '#':
                self.event_channel_msg(irc_user(tokens[0][1:]),tokens[2],
                                       raw[raw.find(':',1)+1:])
            else:
                self.event_priv_msg(irc_user(tokens[0][1:]),
                                    raw[raw.find(':',1)+1:])
        
        elif len(tokens) >= 5 and tokens[1].lower() == 'kick':
            self.event_kick(irc_user(tokens[0][1:]),tokens[3],
                                tokens[2],raw[raw.find(':',1)+1:])
        
        elif len(tokens) == 3 and tokens[1].lower() == 'nick':
            new_nick=tokens[2][1:]
             
            if self.nick == irc_user(tokens[0][1:]).get_nick():
                self.nick=new_nick

            self.event_nick(irc_user(tokens[0][1:]), new_nick)

        elif len(tokens) >= 5 and tokens[1].lower() == 'mode':
            if tokens[3] == '+o':
                self.event_op(irc_user(tokens[0][1:]),tokens[2],
                               tokens[4])
            if tokens[3] == '-o':
                self.event_deop(irc_user(tokens[0][1:]),tokens[2],
                                 tokens[4])
            if tokens[3] == '+v':
                self.event_voice(irc_user(tokens[0][1:]),tokens[2],
                                 tokens[4])
            if tokens[3] == '-v':
                self.event_devoice(irc_user(tokens[0][1:]),tokens[2],
                                   tokens[4])
        
        elif len(tokens) >= 3 and tokens[1].lower() == 'part':
            self.event_part(irc_user(tokens[0][1:]), tokens[2], 
                            raw[raw.find(':',1)+1:])
                     
        elif len(tokens) >= 3 and tokens[1].lower() == 'join':
            self.event_join(irc_user(tokens[0][1:]), tokens[2][1:])
    
        elif len(tokens) >= 2 and tokens[1].lower() == 'kill':
            self.event_kill(irc_user(tokens[0][1:]), raw[raw.find(':',1)+1:])
    
        elif len(tokens) >= 2 and tokens[1].lower() == 'quit':
            self.event_quit(irc_user(tokens[0][1:]), raw[raw.find(':',1)+1:])
    
    def event_ping(self, msg):
        self.send('PONG :'+msg)

    def event_op(self, user, channel, nick_oped):
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' oped '+nick_oped \
                +' in '+channel
        
        self.who(channel)

    def event_deop(self, user, channel, nick_oped):
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' deoped '+nick_oped \
                +' in '+channel
        
        # The user is not op anymore, but it can be voice
        # so, we run a who query to update his situation
        self.who(channel)
        #self.channels[channel][nick_oped].set_status('')

    def event_voice(self, user, channel, nick_oped):
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' voiced '+nick_oped \
                +' in '+channel

        # Because i feel lazy, i just run a who...
        self.who(channel)

    def event_devoice(self, user, channel, nick_oped):
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' devoiced '+nick_oped \
                +' in '+channel
                            
        # The user is not voice anymore, but he can be still op
        # so, we run a who query to update his situation
        self.who(channel)
        #self.channels[channel][nick_oped].set_status('')

    def event_channel_msg(self, user, channel, msg):
        if self.DEBUG:
            print 'DEBUG channel msg @ '+channel+' by '+(user.get_nick()) \
                +': '+msg

    def event_join(self, user, channel):
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
        print self.channels[channel]
    
    def event_part(self, user, channel, msg):
        if self.DEBUG:
            print 'DEBUG ' + (user.get_nick()) + ' left channel ' \
                + channel + '. reason: "' + msg + '"'

        if self.get_nick() == user.get_nick():
            del self.channels[channel]
        elif user.get_nick() in self.channels[channel]:
            del self.channels[channel][user.get_nick()]
        
            if self.DEBUG:
                print self.channels[channel]

    def event_priv_msg(self, user, msg):
        if self.DEBUG:
            print 'DEBUG priv msg by '+(user.get_nick())+': '+msg

    def event_kick(self, user, kicked_nick, chan, msg):
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' kicked '+kicked_nick \
                +' from '+chan+' msg: '+msg

        if (kicked_nick == self.get_nick()):
            print 'I GOT KICKED :('
            del self.channels[chan]
        else:
            print self.channels[chan]
            del self.channels[chan][kicked_nick]
            print self.channels[chan]
    
    def event_nick(self, user, new_nick):
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' changed nick to '+new_nick
        
        # FIXME: This can be done without resorting to /WHO
        for chan in self.channels.keys():
            self.who(chan)


    def event_quit(self, user, reason):
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' has quit. Reason: ' + \
                reason
 
        # FIXME: This can be done without resorting to /WHO
        for chan in self.channels.keys():
            self.who(chan)

    def event_kill(self, user, reason):
        if self.DEBUG:
            print 'DEBUG '+(user.get_nick())+' got killed! Reason: ' + \
                reason

    def make_raw_nick(self, nick, user, host):
        return nick + '!' + user + '@' + host

    def event_numeric(self, event_num, nick, params, msg):
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

            self.channels[chan][nickname] = irc_user(self.make_raw_nick(nickname, username, host))
            self.channels[chan][nickname].set_status(status)

        elif event_num == self.RFC_RPL_ENDOFWHO:
            self.state = ''
                
    def event_socket_closed(self):
        if self.DEBUG:
            print 'DEBUG socket closed'

