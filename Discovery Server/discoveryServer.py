import socket
import sys
sys.path.append('../Server') #TODO: Add this to the configuration?
from server import Server 
from configparser import ConfigParser
import logging
from myTraceback import myTraceback

class discoveryServer(Server):
    def __init__(self, port):
        """Reading the Configuration file & creating the class instances"""
        super().__init__(port, socket.SOCK_DGRAM, "Discovery Server")
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
        self.__HOST = self.__serverConfig['IP']['HOST']
        self.__PORT =self.__serverConfig['IP']['PORT']
        self.__FORMAT = self.__serverConfig ['MSG']['FORMAT']

    def _Server__handle_client(self, client, address):
        """Sending the client the host and port of the current server"""
        chatServerHost = self.__serverConfig['chatServer']['HOST']
        chatServerPort =self.__serverConfig['chatServer']['PORT']
        logging.debug(f'sending to {address[0]},{address[1]}: "{chatServerHost}:{chatServerPort}"')
        client.sendto(f'{chatServerHost}:{chatServerPort}'.encode(self.__FORMAT), (address[0],address[1]))


if __name__ == "__main__":
    s = discoveryServer(6051)
    s.startServer()