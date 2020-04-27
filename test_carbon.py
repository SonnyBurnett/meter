import time
import socket
sock = socket.socket()
sock.connect( ("localhost", 2003) )
sock.send("test.metric 50 %d \n" % time.time())
sock.close()
