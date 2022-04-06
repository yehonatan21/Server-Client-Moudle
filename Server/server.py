#https://docs.python.org/3/howto/sockets.html
#https://docs.python.org/3/library/socket.html

import keyboard
import logging
import socket
import threading
import time
from myTraceback import myTraceback

class Server():
    def restartServer():
        pass #TODO: implemet

    def __init__(self, port, socketType, loggingName = __name__):
        """Reading the Configuration file, creating the class instances and creating costum logging file"""
        self.__port = port
        self.__listener = socket.socket(socket.AF_INET, socketType)
        self.__myTrace = myTraceback()
        self.__running = True
        if(self.__myTrace.is_debug()):
            logging.basicConfig(
                filename=f'{loggingName}-debug.logs',
                level=logging.DEBUG,
                format='%(asctime)s: %(levelname)s: %(message)s'
            )
            import os
            logging.debug(os.getcwd())
        else:
            logging.basicConfig(
                filename=f'{loggingName}.logs',
                level=logging.INFO,
                format='%(asctime)s: %(levelname)s: %(message)s'
        )

    def startServer(self):
        """
        Creating server with the default parameters or with parameters from the chiled class
        """
        host = socket.gethostbyname('')
        logging.info(f'trying to bind on port {self.__port}') 
        self.__listener.bind((host,self.__port))
        isTCP = self.__listener.type == socket.SocketKind.SOCK_STREAM
        logging.debug(f'Is TCP: {isTCP}')
        msg = None
        bufferSize = 1024
        self.__create_threads()
        while self.__running:
            try:
                if isTCP:
                    self.__listener.listen(4)
                    logging.debug(f'TCP Server is running and listening on port {self.__port}...')
                    client, address = self.__listener.accept()
                    logging.debug(f'connection is established with {str(address)}')
                else:
                    logging.debug(f'UDP Server is running on port {self.__port}...')
                    client = self.__listener
                    msg, address  = self.__listener.recvfrom(bufferSize) #msg is decleared for convention 
                thread = threading.Thread(target=self.__handle_client, args=(client, address)) #TODO: send also message - why?
                thread.start()
            except:
                pass
            time.sleep(1)
       
    def stopServer(self):
        while self.__running:
            if keyboard.is_pressed ('ctrl + q'):
                self.__listener.close() 
                print("The server stoped")
                self.__running = False
            time.sleep(1)

    def __handle_client(self, client, address, message=None):
        """This will be implemented in the chiled class"""
        print(message)
        client.sendto(str.encode("SUCCESS"), address)

    def __create_threads(self):
        print("create threads: " + str(self))
        listenToKeyboardEvent = threading.Thread(target=self.stopServer)
        listenToKeyboardEvent.start()

if __name__ == "__main__":
    s = Server()
    s.startServer()
