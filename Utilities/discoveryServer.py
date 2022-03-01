import socket
from server import Server
from configparser import ConfigParser


class discoveryServer(Server(6051,socket.SOCK_DGRAM)): #TODO: Change to UDP - Done.
  
    def __init__(self):
            ipConfig = ConfigParser()
            ipConfig.read('./Utilities/IPconfig.ini')
            self.__HOST = ipConfig['IP']['HOST']
            self.__PORT =ipConfig['IP']['PORT']

    def _Server__handle_client(self, client):
        client.send(f'{self.__HOST}:{self.__PORT}'.encode(self.__FORMAT)) #TODO: move the IP to a configuration file - Done.
        client.close()


if __name__ == "__main__":
    s = discoveryServer(6050)
    s.startServer()