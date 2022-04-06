import logging
import sys
import socket
from configparser import ConfigParser
sys.path.append('../Server')  
from server import Server 
from myTraceback import myTraceback

class PostServer(Server):

    def __init__(self, port):
            super().__init__(port, socket.SOCK_STREAM, "Post Server")
            self.__serverConfig = ConfigParser() #TODO: Change to private or take out to a sepeart moudle - Done?
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

    def _Server__handle_client(self, client, address):
        pass
    
    def getPostFromClinet(post, apps):
        pass

    def __custumToApps(apps):
        pass
    
    def __publishPost():
        pass

    def __isPublishet():
        pass

    def __postPreview():
        pass

if __name__ == "__main__":
    s = PostServer(6053)
    s.startServer()
