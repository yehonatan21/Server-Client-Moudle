#https://docs.python.org/3/howto/sockets.html
#https://docs.python.org/3/library/socket.html

import socket
import threading
# import getTraceback
import logging
# import os
# print(os.getcwd())

# TODO: kill the server 


# def get_traceback(e): #TODO: Take out to separeated moudle - Done.
#     lines = traceback.format_exception(type(e), e, e.__traceback__)
#     return ''.join(lines)

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
        logging.basicConfig(
            filename=f'{loggingName}.logs',
            level=logging.DEBUG,
            format='%(asctime)s: %(levelname)s: %(message)s'
        )
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
