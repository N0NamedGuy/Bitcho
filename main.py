#! /usr/bin/env python2.7

from bitcho import Bitcho
import sys

host='irclei.ath.cx'
port=6667

nick = sys.argv[1] if len(sys.argv) >= 2 else 'bot-testing'
password= sys.argv[2] if len(sys.argv) >= 3 else "blahbottesting"

channels=[]
if len(sys.argv) >= 4:
    channels = sys.argv[3:]
else:
    channels=['#bot-events']

def main():
    auth=(nick,password)
    client=Bitcho(host,port,auth,channels)
    try:
        client.connect()
        client.nick(nick)
        client.send_welcome()
        client.join_channels()
        client.recv_loop()
    except KeyboardInterrupt:
            client.quit('Hasta!')
            client.close()
            print
            print 'socket closed'
    except Exception, e:
            client.quit('I made a boo boo =(')
            client.close()
            print 'socket closed'
            print e
            raise

main()