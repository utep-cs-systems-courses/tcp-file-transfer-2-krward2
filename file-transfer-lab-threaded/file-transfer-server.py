#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
from framedSock import framedReceive
from threading import Thread
from threading import Lock

sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False),
    (('-d', '--debug'), 'debug', 0) # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces
debug = paramMap['debug']

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(16)
# s is a factory for connected sockets

lock = Lock()

def receiveFile(connection):
    try:
        fileName, contents = framedReceive(conn, debug)
    except:
        print("Error: File transfer was not successful!")
        conn.sendall(str(0).encode())
        sys.exit(1)
    if not os.path.exists("./files-received"):
        os.makedirs("./files-received")

    fileName = fileName.decode()

    lock.acquire()
    with open("./files-received/"+fileName, 'w+b') as f:
        file = f.write(contents)
    lock.release()

    conn.sendall(str(1).encode())
    sys.exit()

while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    print('Connected by', addr)
    fileReceiveThread = Thread(target=receiveFile, args=(conn,))
    fileReceiveThread.start()
