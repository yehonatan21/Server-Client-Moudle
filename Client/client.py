import socket
import threading
from configparser import ConfigParser


#TODO: Remove all code and leave only a class

class Client():

    def __init__(self, nick, password):
        #TODO: Take out to configuration - Done
        self.__stop_loops = False
        ipConfig = ConfigParser()
        ipConfig.read('./Utilities/IPconfig.ini')
        self.__HOST = ipConfig['IP']['HOST']
        self.__PORT =ipConfig['IP']['PORT']
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__HOST,self.__PORT))

    def __printToUser(self, message):
        print(message)

    def __receive_message(self):
        while True:
            if self.__stop_loops:
                break
            try:
                message = self.__client.recv(1024).decode(self.__FORMAT) #TODO: make it match insted of if-else
                if message == 'nickname':
                    self.__client.send(self.__nickname.encode(self.__FORMAT))
                    message = self.__client.recv(1024).decode(self.__FORMAT)
                    if message  == 'PASS':
                        self.__client.send(self.__password.encode(self.__FORMAT))
                        message = self.__client.recv(1024).decode(self.__FORMAT)
                        if message == 'Refuse':
                            self.__printToUser('Connection refused. Wrong password!')
                            self.__stop_loops = True
                        else:
                            self.__printToUser(message) 
                    else:
                        self.__printToUser(message) 
                else:
                    self.__printToUser(message) 
                if message == 'You have discinnected successfully.' or 'Refuse' or 'You left the chat room' or 'You have been kicket from the chat room': #FIXME: OR is not working
                    self.__stop_loops = True
                if message == '':
                    self.__printToUser('The server is down. Click enter to exit.')
                    self.__client.close()
                    self.__stop_loops = True
                if message == 'IP':
                    self.__client.send('send'.encode(self.__FORMAT))
                    serverIP = self.__client.recv(1024).decode(self.__FORMAT)
                    self.__client.close()
                    self.__connectServer(serverIP)
            except Exception as e:
                self.__printToUser(e)
                self.__printToUser('An error occured!')
                self.__client.close()
                self.__stop_loops = True

    def __write_message(self): #FIXME: how can i immediately breakthis loop like rhe recive loop without pressing the enter buttom
        while True:
            if self.__stop_loops:
                break
            message = f'{input("")}'
            self.__client.send(message.encode(self.__FORMAT))
    
    def __connectServer(self, serverIP):
        self.__client.connect((serverIP,self.__PORT))

    def create_thread(self):
        receive_thread = threading.Thread(target=self.__receive_message)
        receive_thread.start()

        write_thread = threading.Thread(target=self.__write_message)
        write_thread.start() 

#TODO: Add if main and run all the code from there - Done.
if __name__ == "__main__":
    nickname = input('what is your nickname?\n')
    if nickname == 'admin':
        password = input('Plese enter the password:\n')
    c = Client(nickname,password)
    c.create_thread()