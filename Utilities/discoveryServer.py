from server import Server
import socket
import threading

class discoveryServer(Server):
  

     def _Server__handle_client(self, client):
        client.send('IP'.encode(self.FORMAT))
        if client.recv(1024).decode(self.FORMAT) == 'send':
            client.send('127.0.0.1'.encode(self.FORMAT))
        client.close()


if __name__ == "__main__":
    s = discoveryServer()
    s.startServer()