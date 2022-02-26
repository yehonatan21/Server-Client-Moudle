import socket
import threading
import sys
import traceback


# BUG: how to kill a server

def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)

class Server():
    port = None# = 6050
    FORMAT = 'utf-8'
    # listener = None
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   

    def __init__(self, port = 6050):
        # body of the constructor
        self.port = port

    def startServer(self):
        host = socket.gethostbyname('')
        self.listener.bind((host, self.port))
        self.listener.listen(4)
        self.__receiveConnections()

    __clientnick = {}  # FIXME: to replace the keys and the values

    def __broadcast(self, message, sender=None):
        for client in self.__clientnick:
            if self.__clientnick.get(sender) != self.__clientnick.get(client):
                client.send(message.encode(self.FORMAT))

    def __handle_client(self, client):
        client.send('nickname'.encode(self.FORMAT))
        nickname = client.recv(1024).decode(self.FORMAT)
        if self.__if_nickname_exist(nickname, client):
            return
        if self.__if_admin(client, nickname):
            return
        self.__clientnick[client] = nickname
        print(f'The nickname of this client is {self.__clientnick[client]}')
        if nickname != 'admin':
            client.send('you are now connected!'.encode(self.FORMAT))
        self.__broadcast(
            f'{self.__clientnick[client]} has connected to the chat room!', client)
        while True:
            try:
                message = client.recv(1024).decode(self.FORMAT)
                if self.__handle_messsage(message, client):
                    break
            except Exception as e:
                get_traceback(e)
                print(e)
                # BUG: after kicking the client the server is trying to acsses it.
                client.send('You left the chat room'.encode(self.FORMAT))
                self.__broadcast(
                    f'{self.__clientnick[client]} has left the chat room!')
                del self.__clientnick[client]
                client.close()
                break

    def __if_admin(self, client, nickname):
        if nickname == 'admin':
            client.send('PASS'.encode(self.FORMAT))
            password = client.recv(1024).decode(self.FORMAT)
            if password != 'admin123':
                client.send('Refuse'.encode(self.FORMAT))
                client.close()
                return True
            else:
                client.send(
                    'You logged in as an administrator.'.encode(self.FORMAT))

    def __if_nickname_exist(self, nickname, client):
        for checkclient in self.__clientnick:
            if nickname == self.__clientnick.get(checkclient):
                client.send('This nickname is already exist. Please send a new nickname'.encode(
                    self.FORMAT))  # TODO: insted of diconnection let the client choose another nickname
                client.close()
                return True

    def __handle_messsage(self, message, client):
        if message == '/exit':
            exit_message = 'You have discinnected successfully.'
            self.__close_connection(exit_message, client)
            return True

        if message.startswith('/kick'):  # FIXME: admin functions
            if self.__clientnick.get(client) == 'admin':

                for check_client in self.__clientnick:
                    nickname = message[6:len(message)]
                    # self.__clientnick(nickname)
                    if self.__clientnick.get(check_client) == nickname:
                        kick_message = 'You have been kicket from the chat room.'
                        self.__close_connection(kick_message, check_client)
                        return True
            else:
                client.send('You are not admin!'.encode(self.FORMAT))

        else:
            message = f'{self.__clientnick[client]}:{message}'
            self.__broadcast(message, client)

    def __close_connection(self, message, client):
        print(client)
        client.send(message.encode(self.FORMAT))
        self.__broadcast(
            f'{self.__clientnick[client]} has left the chat room!', client)
        del self.__clientnick[client]
        client.close()

    def __receiveConnections(self):
        print(f'Server is running and listening on port {self.port}...')
        while True:
            client, address = self.listener.accept()
            print(f'connection is established with {str(address)}')
            thread = threading.Thread(
                target=self.__handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    s = Server()
    s.startServer()