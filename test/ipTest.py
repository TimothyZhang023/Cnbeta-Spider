__author__ = 'TianShuo'
import socket
import uuid

myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)
print myname
print myaddr


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


print get_mac_address()
