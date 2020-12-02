#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False),
    (('-f', '--file'), "file", 'send-test-short') # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug, file  = paramMap["server"], paramMap["usage"], paramMap["debug"], paramMap["file"]

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

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

with open(file, 'r') as f:
    file = f.read()
framedSend(s, file.encode(), debug)
