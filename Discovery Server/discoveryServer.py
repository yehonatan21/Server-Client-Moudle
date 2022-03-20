#FIXME: create log file for all the flies in the program acorrdinig to ther name, and add date and time (with ms) - Done.
# from ctypes.wintypes import MSG
import socket
import os #TODO: Import only when debug
print(os.getcwd()) #TODO: change to logging
import sys
sys.path.append('../Server') #TODO: Add this to the configuration?
from server import Server 
from configparser import ConfigParser

class discoveryServer(Server):
    def __init__(self, port):
        super().__init__(port, socket.SOCK_DGRAM, "Discovery Server")
        self.serverConfig = ConfigParser() #TODO: Change to private or take out to a sepeart moudle?
        
        readConfig = self.serverConfig.read('./config.ini')
        try:
            if len(readConfig) == 0:
                raise NameError("No configuration file")#TODO: Put a normal exception OR decide what happens if no configuration exists - NameError: No configuration file - Done.
        except:
            print("The configuration file is empty")
        self.__HOST = self.serverConfig['IP']['HOST']
        self.__PORT =self.serverConfig['IP']['PORT']
        self.__FORMAT = self.serverConfig ['MSG']['FORMAT']

    def _Server__handle_client(self, client, address):
        chatServerHost = self.serverConfig['chatServer']['HOST']
        chatServerPort =self.serverConfig['chatServer']['PORT']
        print(f'sending to {address[0]},{address[1]}: "{chatServerHost}:{chatServerPort}"')
        client.sendto(f'{chatServerHost}:{chatServerPort}'.encode(self.__FORMAT), (address[0],address[1]))


if __name__ == "__main__":
    s = discoveryServer(6051)
    s.startServer()