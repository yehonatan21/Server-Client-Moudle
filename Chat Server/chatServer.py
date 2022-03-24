import logging
import sys
import socket
from configparser import ConfigParser
sys.path.append('../Server')  
from server import Server 
from getTraceback import getTracbace

# import os #TODO: Import only when debug
# print(os.getcwd()) #TODO: change to logging

#TODO: send codes insted of strings to the client - JSON?
#TODO: documaent all the code using pydoc - https://docs.python.org/3/library/pydoc.html

class ChatServer(Server):
    def __init__(self, port):
            super().__init__(port, socket.SOCK_STREAM, "Chat Server")
            self.__serverConfig = ConfigParser() #TODO: Change to private or take out to a sepeart moudle?
            self.__readserverConfig = self.__serverConfig.read('./config.ini')
            self.__myTrace = getTracbace()
            if(self.__myTrace.is_debug()):
                import os #TODO: Import only when debug - Done.
                logging.debug(os.getcwd()) #TODO: change to logging - Done.
            try:
                if len(self.__readserverConfig) == 0:
                    raise NameError("No configuration file")#TODO: Put a normal exception OR decide what happens if no configuration exists - NameError: No configuration file  Done.
            except:
                print("The configuration file is empty")
            self.__FORMAT = self.__serverConfig ['MSG']['FORMAT']
            self.__clientnick = {}

    # def is_debug(self):
    #     gettrace = getattr(sys, 'gettrace', None)

    #     if gettrace is None:
    #         return False
    #     else:
    #         v = gettrace()
    #         if v is None:
    #             return False
    #         else:
    #             return True

    def __broadcast(self, message, sender=None):
        for client in self.__clientnick:
            if self.__clientnick.get(sender) != self.__clientnick.get(client):
                client.send(message.encode(self.__FORMAT))

    def _Server__handle_client(self, client, address):
        client.send('nickname'.encode(self.__FORMAT))
        nickname = client.recv(1024).decode(self.__FORMAT)
        if self.__if_nickname_exist(nickname, client):
            return
        if self.__if_admin(client, nickname):
            return
        self.__clientnick[client] = nickname
        # logging.info(f'The nickname of this client is {self.__clientnick[client]}')
        if nickname != 'admin':
            client.send('you are now connected!'.encode(self.__FORMAT))
        self.__broadcast(
            f'{self.__clientnick[client]} has connected to the chat room!', client)
        while True:
            try:
                message = client.recv(1024).decode(self.__FORMAT)
                if self.__handle_messsage(message, client):
                    break
            except Exception as e:
                self.__myTrace.get_traceback(e)
                logging.info(e)
                # BUG: after kicking the client the server is trying to acsses it.
                client.send('You left the chat room'.encode(self.__FORMAT))
                self.__broadcast(
                    f'{self.__clientnick[client]} has left the chat room!')
                del self.__clientnick[client]
                client.close()
                break

    def __if_admin(self, client, nickname):
        if nickname == 'admin':
            client.send('PASS'.encode(self.__FORMAT))
            password = client.recv(1024).decode(self.__FORMAT)
            if password != 'admin123':
                client.send('Refuse'.encode(self.__FORMAT))
                client.close()
                return True
            else:
                client.send(
                    'You logged in as an administrator.'.encode(self.__FORMAT))

    def __if_nickname_exist(self, nickname, client):
        for checkclient in self.__clientnick:
            if nickname == self.__clientnick.get(checkclient):
                client.send('This nickname is already exist. Please send a new nickname'.encode(self.__FORMAT))  # FIXME: insted of disconnection let the client choose another nickname
                client.close()
                return True

    def __handle_messsage(self, message, client):
        if message == '/exit':
            exit_message = 'You have discinnected successfully.'
            self.__close_connection(exit_message, client)
            return True

        if message.startswith('/kick'):  # TODO: admin functions
            if self.__clientnick.get(client) == 'admin':

                for check_client in self.__clientnick:
                    nickname = message[6:len(message)]
                    # self.__clientnick(nickname)
                    if self.__clientnick.get(check_client) == nickname:
                        kick_message = 'You have been kicket from the chat room.'
                        self.__close_connection(kick_message, check_client)
                        return True
            else:
                client.send('You are not admin!'.encode(self.__FORMAT))

        else:
            message = f'{self.__clientnick[client]}:{message}'
            self.__broadcast(message, client)

    def __close_connection(self, message, client):
        # logging.debug(client)
        client.send(message.encode(self.__FORMAT))
        self.__broadcast(
            f'{self.__clientnick[client]} has left the chat room!', client)
        del self.__clientnick[client]
        client.close()


if __name__ == "__main__":
    s = ChatServer(6052)
    s.startServer()