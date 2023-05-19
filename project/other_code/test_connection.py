import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('123.1.1.2', 22))
    print("Port 22 reachable")
except socket.error as e:
    print('"Error on connect: %s"' % e)
s.close()