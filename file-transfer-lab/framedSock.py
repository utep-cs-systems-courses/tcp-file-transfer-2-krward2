import re


def framedSend(sock, payload, filename, debug=0):
    if debug: print("framedSend: sending %d byte message" % len(payload))
    msg = str(len(payload)).encode()+ b':' + filename + b':' + payload
    while len(msg):
        nsent = sock.send(msg)
        msg = msg[nsent:]


rbuf = b""  # static receive buffer


def framedReceive(sock, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    print("Entering receive")
    while True:
        if (state == "getLength"):
            print("Entering getLength state")
            match = re.match(b'([^:]+):(.*):(.*)', rbuf, re.DOTALL | re.MULTILINE)  # look for colon
            if match:
                lengthStr, fileName, rbuf = match.groups()
                try:
                    msgLength = int(lengthStr)
                except:
                    if len(rbuf):
                        print("badly formed message length:", lengthStr)
                        return None
                state = "getPayload"
        if state == "getPayload":
            print("Entering getPayload state")
            if len(rbuf) >= msgLength:
                payload = rbuf[0:msgLength]
                rbuf = rbuf[msgLength:]
                return fileName, payload
        print("Receiving")
        r = sock.recv(100)
        rbuf += r
        if len(r) == 0:
            if len(rbuf) != 0:
                print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
            return None
        if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
