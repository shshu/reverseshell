import struct

def sendAll(client, data):
        msg = struct.pack('>I', len(data)) + data
        client.sendall(msg)

def recvAll(client):
    # Read message length and unpack it into an integer
    raw_msglen = recvAllHelper(client, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvAllHelper(client, msglen)

def recvAllHelper(client, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = client.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
