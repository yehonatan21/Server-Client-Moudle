#FIXME: create log file for all the flies in the program acorrdinig to ther name, and add date and time (with ms) - Done.
# from ctypes.wintypes import MSG
import socket
import sys
sys.path.append('../Server') #TODO: Add this to the configuration?
from server import Server 
from configparser import ConfigParser
import logging
from myTraceback import myTraceback

class discoveryServer(Server):
    def __init__(self, port):
        super().__init__(port, socket.SOCK_DGRAM, "Discovery Server")
        self.__serverConfig = ConfigParser() #TODO: Change to private or take out to a sepeart moudle? - Done
        self.__readserverConfig = self.__serverConfig.read('./config.ini')
        self.__myTrace = myTraceback()
        if(self.__myTrace.is_debug()):
                import os #TODO: Import only when debug - Done.
                logging.debug(os.getcwd()) #TODO: change to logging - Done.
        try:
            if len(self.__readserverConfig) == 0:
                raise NameError("No configuration file")#TODO: Put a normal exception OR decide what happens if no configuration exists - NameError: No configuration file - Done.
        except:
            print("The configuration file is empty")
        self.__HOST = self.__serverConfig['IP']['HOST']
        self.__PORT =self.__serverConfig['IP']['PORT']
        self.__FORMAT = self.__serverConfig ['MSG']['FORMAT']

    def _Server__handle_client(self, client, address):
        chatServerHost = self.__serverConfig['chatServer']['HOST']
        chatServerPort =self.__serverConfig['chatServer']['PORT']
        logging.debug(f'sending to {address[0]},{address[1]}: "{chatServerHost}:{chatServerPort}"')
        client.sendto(f'{chatServerHost}:{chatServerPort}'.encode(self.__FORMAT), (address[0],address[1]))


if __name__ == "__main__":
    s = discoveryServer(6051)
    s.startServer()