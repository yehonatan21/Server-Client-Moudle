import socket
from server import Server
from configparser import ConfigParser


class discoveryServer(Server): #TODO: Change to UDP - Done.
  
    def __init__(self, port):
        super().__init__(port, socket.SOCK_DGRAM)
        ipConfig = ConfigParser()
        ipConfig.read('./Utilities/config.ini')
        self.__HOST = ipConfig['IP']['HOST']
        self.__PORT =ipConfig['IP']['PORT']

    def _Server__handle_client(self, client, address, message= None):
        client.sendTo(f'{self.__HOST}:{self.__PORT}'.encode(self.__FORMAT), address) #TODO: move the IP to a configuration file - Done.
        client.close()


if __name__ == "__main__":
    s = discoveryServer(6051)
    s.startServer()