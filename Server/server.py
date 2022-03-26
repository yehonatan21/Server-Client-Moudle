#https://docs.python.org/3/howto/sockets.html
#https://docs.python.org/3/library/socket.html

import socket
import threading
import logging
from myTraceback import myTraceback


#TODO: kill the server with keybaerd event
#TODO: Change all prints in all modules to logging - https://docs.python.org/3/howto/logging.html - Done.

class Server():
    def startServer(): 
        pass
    
    def stopServer():
        pass
    
    def restartServer():
        pass

    def __init__(self, port, socketType, loggingName = __name__):
        self.__port = port
        self.__listener = socket.socket(socket.AF_INET, socketType)
        self.__myTrace = myTraceback()
        if(self.__myTrace.is_debug()):
            logging.basicConfig(
                filename=f'{loggingName}-debug.logs',
                level=logging.DEBUG,
                format='%(asctime)s: %(levelname)s: %(message)s'
            )
            import os #TODO: Import only when debug - Done.
            logging.debug(os.getcwd()) #TODO: change to logging - Done.
        else:
            logging.basicConfig(
                filename=f'{loggingName}.logs',
                level=logging.INFO,
                format='%(asctime)s: %(levelname)s: %(message)s'
            )

    def startServer(self):
        host = socket.gethostbyname('')
        logging.info(f'trying to bind on port {self.__port}') #FIXME: logging level - INFO - Done.
        self.__listener.bind((host,self.__port))
        isTCP = self.__listener.type == socket.SocketKind.SOCK_STREAM
        logging.debug(f'Is TCP: {isTCP}') #FIXME: logging level - debug - Done.
        msg = None
        bufferSize = 1024
        while True:
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
        
    def __handle_client(self, client, address, message=None):
        print(message)
        client.sendto(str.encode("SUCCESS"), address)

if __name__ == "__main__":
    s = Server()
    s.startServer()
