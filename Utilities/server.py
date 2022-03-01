#https://docs.python.org/3/howto/sockets.html
#https://docs.python.org/3/library/socket.html

import socket
import threading
import traceback
import logging
# BUG: how to kill a server


def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)

#TODO: Change all prints in all modules to logging - https://docs.python.org/3/howto/logging.html
class Server():
    #TODO: Change to private - Done.
    # __port = None
    # __FORMAT = 'utf-8'
    # __listener = None
   

    def __init__(self, port = 6050, socketType = socket.SOCK_STREAM): #TODO: Remove the default values when the right time will come
        # body of the constructor
        self.__port = port
        self.__listener = socket.socket(socket.AF_INET, socketType)
        logging.basicConfig(
        filename='server.logs',
        level=logging.INFO,
        format='%(levelname)s:%(message)s'
        )

    def startServer(self):
        
        host = socket.gethostbyname('')
        self.__listener.bind((host,self.__port))
        if self.__listener.type == socket.SocketKind.SOCK_STREAM:
            self.__listener.listen(4)
        self.__receiveConnections()

    def __receiveConnections(self):
        logging.info(f'Server is running and listening on port {self.__port}...')
        while True:
            client, address = self.__listener.accept() #TODO: Check the option to take this out of the loop
            logging.info(f'connection is established with {str(address)}')
            thread = threading.Thread(target=self.__handle_client, args=(client,)) #BUG: to fix the target __handle_client to work in the chatServer - Done.
            thread.start()


if __name__ == "__main__":
    s = Server()
    s.startServer()
