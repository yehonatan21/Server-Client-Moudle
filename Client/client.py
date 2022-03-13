import socket
import threading
from configparser import ConfigParser
import os
print(os.getcwd())


#TODO: Remove all code and leave only a class - Done.

class Client():

    def __init__(self, nick, password = None):
        #TODO: Take out to configuration - Done
        self.__nickname = nick
        self.__password = password
        self.__stop_loops = False
        readConfig = ConfigParser()#TODO: Change the variable name - Done.
        readConfig.read('./config.ini') #TODO: add config check
        print(readConfig.sections())
        self.__DISCOVERY_IP = readConfig['DiscoveryServer']['IP']
        self.__DISCOVERY_PORT = int(readConfig['DiscoveryServer']['PORT'])
        self.__FORMAT = readConfig['Client']['FORMAT']
        print(self.__DISCOVERY_IP)
        print(self.__DISCOVERY_PORT)

    def connectClientToServer(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Send to server using created UDP socket
        serverAddressPort = (self.__DISCOVERY_IP, self.__DISCOVERY_PORT)
        self.__client.sendto(str.encode("KK"), serverAddressPort)
        bufferSize = 1024
        msgFromServer = self.__client.recvfrom(bufferSize) #FIXME: Make this work against the discovery server - Done.
        # print(type(msgFromServer))
        # print(msgFromServer[1])
        msg = msgFromServer[0].decode(self.__FORMAT)
        print(f'Message from Server: {msg}')
        connectionInfo = msg.split(':')
        self.__HOST = connectionInfo[0]
        self.__PORT = int(connectionInfo[1])
        print(f'About to connect to: {self.__HOST}:{self.__PORT}')
        # print(self.__HOST)
        # print(self.__PORT)
        
        #TODO: Config files need to be fixed to be without strings - Done.
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'trying to connect to {self.__HOST}:{self.__PORT}')
        self.__client.connect((self.__HOST,self.__PORT)) #FIXME: Need to run the both the chatServer and the discoveryServer.
        print(f'connected succefuly to {self.__HOST}:{self.__PORT}')
        self.__create_thread()
        
    def __printToUser(self, message):
        print(message)

    def __receive_message(self):
        while True:
            if self.__stop_loops:
                break
            try:
                message = self.__client.recv(1024).decode(self.__FORMAT) #TODO: make it match insted of if-else?
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
            if self.__stop_loops:# BUG: Not Working
                break
            message = f'{input("")}'
            self.__client.send(message.encode(self.__FORMAT))
    
    def __connectServer(self, serverIP):
        self.__client.connect((serverIP,self.__PORT))

    def __create_thread(self):
        #Connect to discovery server
        #TODO: Make this self explantory - Done
        receive_thread = threading.Thread(target=self.__receive_message)
        receive_thread.start()

        write_thread = threading.Thread(target=self.__write_message)
        write_thread.start() 

#TODO: Add if main and run all the code from there - Done.
if __name__ == "__main__":
    # nickname = input('what is your nickname?\n')
    nickname = "TEST"
    password = None
    if nickname == 'admin':
        password = input('Plese enter the password:\n')
    c = Client(nickname,password)
    c.connectClientToServer()