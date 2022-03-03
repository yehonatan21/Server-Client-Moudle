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

#TODO: Change all prints in all modules to logging - https://docs.python.org/3/howto/logging.html - Done.
class Server():
   

    def __init__(self, port = 6050, socketType = socket.SOCK_STREAM): #TODO: Remove the default values when the right time will come
        print('1')
        #TODO: Change to private - Done.
        self.__port = port
        print('2')
        self.__listener = socket.socket(socket.AF_INET, socketType)
        print('3')
        logging.basicConfig(
            filename='server.logs',
            level=logging.INFO,
            format='%(levelname)s:%(message)s'
        )
        print('4')

    def startServer(self):
        print('5')
        host = socket.gethostbyname('')
        print('6')
        self.__listener.bind((host,self.__port))
        print('7')
        isTCP = self.__listener.type == socket.SocketKind.SOCK_STREAM
        message = None
        bufferSize  = 1024
        while True:
            if isTCP:
                self.__listener.listen(4)
                logging.info(f'TCP Server is running and listening on port {self.__port}...')
                client, address = self.__listener.accept() #TODO: Check the option to take this out of the loop
                logging.info(f'connection is established with {str(address)}')
            else:
                logging.info(f'UDP Server is running and listening on port {self.__port}...')
                client = self.__listener
                bytesAddressPair  = client.recvfrom(bufferSize) #TODO: Change the syntax to be like the accept
                message = bytesAddressPair[0]
                address = bytesAddressPair[1]
            thread = threading.Thread(target=self.__handle_client, args=(client, address, message)) #BUG: to fix the target __handle_client to work in the chatServer - Done.
            thread.start()
            print('8')
        print("9")     
        
    def __handle_client(self, client, address, message):
        print(message)
        client.sendto(str.encode("SUCCESS"), address)

if __name__ == "__main__":
    print("Start1")
    s = Server()
    print("Start2")
    s.startServer()
    print("Start3")
