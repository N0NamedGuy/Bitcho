#! /usr/bin/env python2.7

from bitcho import Bitcho
import sys

host = 'irclei.ath.cx'
port = 6667

if len(sys.argv) > 1:
    host = sys.argv[1]

if len(sys.argv) > 2:
    port = sys.argv[2]

def main():
    client=Bitcho(host,port)
    try:
        client.connect()
        client.recv_loop()
    except KeyboardInterrupt:
        client.quit('Hasta!')
        client.close()
        print
        print 'socket closed'
    except Exception as e:
        client.quit('I made a boo boo =(')
        client.close()
        print 'socket closed'
        print e
        raise

main()
