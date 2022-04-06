#https://docs.python.org/3/howto/sockets.html
#https://docs.python.org/3/library/socket.html

from configparser import ConfigParser
import keyboard
import logging
import socket
import threading
import time
from myTraceback import myTraceback

class Server():

    def __init__(self, port, socketType, loggingName = __name__):
        """Reading the Configuration file, creating the class instances, creating costum logging file and reading the configuration file"""
        self.__port = port
        self.__listener = socket.socket(socket.AF_INET, socketType)
        self.__myTrace = myTraceback()
        self.__running = True
        self.__createLoggingFiles(loggingName)
        self.__readConfig()

    def __createLoggingFiles(self,loggingName):
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

    def __readConfig(self):
        self.__serverConfig = ConfigParser()
        __readserverConfig = self.__serverConfig.read('./config.ini')
        self.__myTrace = myTraceback()
        if(self.__myTrace.is_debug()):
                import os
                logging.debug(os.getcwd())
        try:
            if len(__readserverConfig) == 0:
                raise NameError("No configuration file")
        except:
            print("The configuration file is empty")
    
    def startServer(self):
        """
        Creating server with the default parameters or with parameters from the chiled class
        """
        host = self.__serverConfig['IP']['HOST']
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
                break
            # time.sleep(1)
        
    def __handle_client(self, client, address, message=None):
        """This will be implemented in the chiled class"""
        print(message)
        client.sendto(str.encode("SUCCESS"), address)

    def __create_threads(self):
        logging.info("create threads: " + str(self))
        stopServerKeyboardEvent = threading.Thread(target=self.stopServer)
        stopServerKeyboardEvent.start()

if __name__ == "__main__":
    s = Server()
    s.startServer()
