import logging
import sys
import socket
from configparser import ConfigParser
sys.path.append('../Server')  
from server import Server 
from myTraceback import myTraceback

#TODO: send codes insted of strings to the client - JSON?
#TODO: documaent all the code using pydoc - https://docs.python.org/3/library/pydoc.html

class ChatServer(Server):
    def __init__(self, port):
        """
        Reading the Configuration file and creating the class instances
        :param `port`: the port that the server is running on
        """
        super().__init__(port, socket.SOCK_STREAM, "Chat Server")
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
        self.__FORMAT = self.__serverConfig ['MSG']['FORMAT']
        self.__clientnick = {}

    def __broadcast(self, message, sender=None):
        """
        Brodcast the message to all clients
        :param message: the message from bla bla
        :param sender: the sender of the bla bla
        """
        for client in self.__clientnick:
            if self.__clientnick.get(sender) != self.__clientnick.get(client):
                client.send(message.encode(self.__FORMAT))

    def _Server__handle_client(self, client, address):
        """Adding the client to the connected client's doctionery"""

        client.send('nickname'.encode(self.__FORMAT))
        nickname = client.recv(1024).decode(self.__FORMAT)
        if self.__if_nickname_exist(nickname, client):
            return
        if self.__if_admin(client, nickname):
            return
        self.__clientnick[client] = nickname
        logging.debug(f'The nickname of this client is {self.__clientnick[client]}')
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
        """Checking if the this client is the admin"""
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
        """Checking if the there is a connected client with this name"""
        for checkclient in self.__clientnick:
            if nickname == self.__clientnick.get(checkclient):
                client.send('This nickname is already exist.Plese connect again'.encode(self.__FORMAT))  # FIXME: insted of disconnection let the client choose another nickname
                client.close()
                return True

    def __handle_messsage(self, message, client):
        """Checking if the message is a commend"""
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
        """Closing the connection between the server and the client"""
        # logging.debug(client)
        client.send(message.encode(self.__FORMAT))
        self.__broadcast(
            f'{self.__clientnick[client]} has left the chat room!', client)
        del self.__clientnick[client]
        client.close()

if __name__ == "__main__":
    s = ChatServer(6052)
    s.startServer()