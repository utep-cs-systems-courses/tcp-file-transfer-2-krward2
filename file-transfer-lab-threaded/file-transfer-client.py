#! /usr/bin/env python3

from framedSock import framedSend

# Echo client program
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), 'usage', False),
    (('-d', '--debug'), 'debug', 0) # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)
server, usage, debug = paramMap['server'], paramMap['usage'], paramMap['debug']

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

clientSocket = socket.socket(addrFamily, socktype)
clientSocket.connect(addrPort)

while True:
    fileName = input("Enter the file's name: ")

    if fileName == 'exit':
        sys.exit()
    else:
        if not fileName:
            continue
        elif os.path.exists("./files/"+fileName):

            with open("./files/"+fileName, 'r+b') as f:
                fileContents = f.read()

            #Empty file check
            if len(fileContents) < 1:
                print("Empty file")
                continue
            framedSend(clientSocket, fileContents, fileName.encode(), debug)
            status = int(clientSocket.recv(1).decode())

            if status:
                print("File transfered successfully")
                sys.exit()
            else:
                print("File not sent successfully")
                sys.exit()
        else:
            print("No such file")
