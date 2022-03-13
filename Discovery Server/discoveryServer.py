#FIXME: create log file for all the flies in the program acorrdinig to ther name, and add date and time(with ms).

from ctypes.wintypes import MSG
import socket
# import path
import os
import sys 
sys.path.append('./Server') #TODO: Add this to the configuration - can it be?
sys.path.append("C:\\Users\\User\\Desktop\\Car-Race\\Server") #FIXME: Can't run from cmd like sys.path.append('./Server'
from server import Server #BUG: Can't run from cmd - need to write all the directory in  the sys.path.append
from configparser import ConfigParser
import os
print(os.getcwd())


class discoveryServer(Server): #TODO: Change to UDP - Done.
  
    def __init__(self, port):
        super().__init__(port, socket.SOCK_DGRAM)
        self.serverConfig = ConfigParser()
        
        readFile = self.serverConfig.read('./config.ini')
        if len(readFile) == 0:
            raise NameError("No configuration file")#TODO: Put a normal exception OR decide what happens if no configuration exists - Done.
        self.__HOST = self.serverConfig['IP']['HOST']
        self.__PORT =self.serverConfig['IP']['PORT']
        self.__FORMAT = self.serverConfig ['MSG']['FORMAT']

    def _Server__handle_client(self, client, address):
        chatServerHost = self.serverConfig['chatServer']['HOST']
        chatServerPort =self.serverConfig['chatServer']['PORT']
        print(f'sending to {address[0]},{address[1]}: "{chatServerHost}:{chatServerPort}"')
        client.sendto(f'{chatServerHost}:{chatServerPort}'.encode(self.__FORMAT), (address[0],address[1])) #TODO: move the IP to a configuration file - Done.
        # client.close() #BUG: trying to access this clinet in the Server class after closing the connection


if __name__ == "__main__":
    s = discoveryServer(6051)
    s.startServer()