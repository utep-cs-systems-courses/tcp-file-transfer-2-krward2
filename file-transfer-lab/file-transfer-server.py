#! /usr/bin/env python3

# Echo server program

import socket, sys, re
from framedSock import framedReceive

sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(16)
# s is a factory for connected sockets

while True:

    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    print('Connected by', addr)
    # receive files from client connection
    if not os.fork():
        try:
            fileName, contents = framedReceive(connection, debug)
        except:
            print("Error: File transfer was not successful!")
            conn.sendAll(str(0).encode())
            sys.exit(1)
        if not os.path("./files-received"):
            os.makedirs("./files-received")

        with open(filename, 'w+b') as f:
            file = f.write(contents)
            file.close()
        conn.sendall(str(1).encode())
        sys.exit()
