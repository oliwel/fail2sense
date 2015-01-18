#!/usr/bin/python 

import socket
import sys
import time
import hashlib
import subprocess
from thread import *
from Crypto.Cipher import AES

AES_KEY = 'secret'

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    sock.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

sock.listen(10)
print 'Socket now listening'

key = hashlib.sha256(AES_KEY).digest();
encobj = AES.new(key, AES.MODE_ECB)

#Function for handling connections
def clientthread(conn):

    #Receiving from client
    data = conn.recv(1024)
    conn.close()
   
    try:
        data = encobj.decrypt(data)
       
        if not data.startswith('X42'):
            raise Exception('Decryption error')

        print "Data " + data 
        rule = data.split(' ')
        
        # check timestamp
        if (abs(int(rule[3]) - int(time.time())) > 5):
            raise Exception('Time is running out')

        print "Do {} host {}".format(rule[1], rule[2]);
        subprocess.call('echo', "Do {} host {}".format(rule[1], rule[2]))
  
    except Exception as inst:
        print "Failed receiving - " + inst.args[0]

#now keep talking with the client
while 1:
    #wait to accept a connection
    conn, addr = sock.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread
    start_new_thread(clientthread ,(conn,))

sock.close()
