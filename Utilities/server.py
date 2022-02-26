import socket
import threading
import sys
import traceback


class Server():
   
    __port = None
    # __listener = None
    __listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    def __init__(self, __port = 6050):
        # body of the constructor
        self.__port = __port

    def startServer(self):
        host = socket.gethostbyname('')
        self.__listener.bind((host, self.__port))
        self.__listener.listen(4)
        self.__receiveConnections()

    def __receiveConnections(self):
        print(f'Server is running and listening on __port {self.__port}...')
        while True:
            client, address = self.__listener.accept()
            print(f'connection is established with {str(address)}')
            thread = threading.Thread(
                target=self.__handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    s = Server()
    s.startServer()