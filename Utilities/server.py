import socket
import threading
import sys
import traceback
# BUG: how to kill a server


def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)


class Server():
    port = None# = 6050
    FORMAT = 'utf-8'
    # listener = None
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   

    def __init__(self, port = 6050):
        # body of the constructor
        self.port = port

    def startServer(self):
        host = socket.gethostbyname('')
        self.listener.bind((host, self.port))
        self.listener.listen(4)
        self.__receiveConnections()

    def __receiveConnections(self):
        print(f'Server is running and listening on port {self.port}...')
        while True:
            client, address = self.listener.accept()
            print(f'connection is established with {str(address)}')
            thread = threading.Thread(
                target=self.__handle_client, args=(client,)) #BUG: to fix the target __handle_client to work in the chatServer
            thread.start()


if __name__ == "__main__":
    s = Server()
    s.startServer()