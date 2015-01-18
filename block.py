#!/usr/bin/python

import socket
import sys
import time
import hashlib
import argparse
from Crypto.Cipher import AES

AES_KEY = 'secret'

# Fetch the ip 
parser = argparse.ArgumentParser()
parser.add_argument("action", help="The action to take, either block or unblock")
parser.add_argument("host", help="The host to block/unblock, (IPv4 address)")
args = parser.parse_args()

print >>sys.stderr, 'connect - {} host {} '.format(args.action, args.host);

sock = socket.create_connection(('localhost', 9999))

try:
    
    # Send data
    message = 'X42 {} {} {}'.format(args.action, args.host, int(time.time()-3)).ljust(32,' ')

    key = hashlib.sha256(AES_KEY).digest();
 
    encobj = AES.new(key, AES.MODE_ECB)
    ciphertext = encobj.encrypt(message)

    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(ciphertext)

    data = sock.recv(16)
    print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()


