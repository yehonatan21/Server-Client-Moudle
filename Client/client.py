import socket
import threading
import logging
from configparser import ConfigParser
from getTraceback import getTracbace

#TODO: send codes insted of strings to the client - JSON?
#TODO: sepeareat to coreClient and clientImplementaion
class Client():
    def __init__(self, nick, password = None): #TODO: Talk about the password
        self.__nickname = nick
        self.__password = password
        self.__stop_loops = False
        logging.basicConfig(
            filename='client.logs',
            level=logging.DEBUG,
            format='%(asctime)s: %(levelname)s: %(message)s'
        )
        self.__myTrace = getTracbace()
        if(self.__myTrace.is_debug()):
            import os #TODO: Import only when debug - Done.
            logging.debug(os.getcwd()) #TODO: change to logging - Done.
        
        clientConfig = ConfigParser()#TODO: Change the variable name - Done
        clientConfig.read('./config.ini') #TODO: add config check - Done.
        try:
            if len(clientConfig) == 0:
                raise NameError("No configuration file")#TODO: Put a normal exception OR decide what happens if no configuration exists - NameError: No configuration file - Done.
        except:
            print("The configuration file is empty")
        self.__DISCOVERY_IP = clientConfig['DiscoveryServer']['IP']
        self.__DISCOVERY_PORT = int(clientConfig['DiscoveryServer']['PORT'])
        self.__FORMAT = clientConfig['Client']['FORMAT']
        # logging.debug(self.__DISCOVERY_IP)
        # logging.debug(self.__DISCOVERY_PORT)

    def connectClientToServer(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Send to server using created UDP socket
        serverAddressPort = (self.__DISCOVERY_IP, self.__DISCOVERY_PORT)
        self.__client.sendto(str.encode("KK"), serverAddressPort)
        bufferSize = 1024
        msgFromServer = self.__client.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(self.__FORMAT)
        logging.debug(f'Message from Discovery Server: "{msg}"')
        connectionInfo = msg.split(':')
        self.__HOST = connectionInfo[0]
        self.__PORT = int(connectionInfo[1])
        logging.debug(f'About to connect to: {self.__HOST}:{self.__PORT}')
        
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug(f'trying to connect to {self.__HOST}:{self.__PORT}')
        self.__client.connect((self.__HOST,self.__PORT))
        logging.debug(f'connected succefuly to {self.__HOST}:{self.__PORT}')
        self.__create_thread()
        
    def __printToUser(self, message):
        print(message)

    def __receive_message(self):
        while True:
            if self.__stop_loops:
                break
            try:
                message = self.__client.recv(1024).decode(self.__FORMAT)
                if message == 'nickname': #TODO: make it match-case insted of if-else?
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
                if message == ('You have discinnected successfully.' or 'Refuse' or 'You left the chat room' or 'You have been kicket from the chat room'): #TODO: get codes insted of strings
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

    def __write_message(self):
        message = None
        while True:
            if self.__stop_loops or message == "/exit":
                break
            message = f'{input("")}'
            self.__client.send(message.encode(self.__FORMAT))
    
    def __connectServer(self, serverIP):
        self.__client.connect((serverIP,self.__PORT))

    def __create_thread(self):
        #Connect to discovery server
        #TODO: Make this self explantory - Done.
        receive_message_thread = threading.Thread(target=self.__receive_message)
        receive_message_thread.start()

        write_message_thread = threading.Thread(target=self.__write_message)
        write_message_thread.start()

if __name__ == "__main__":
    # nickname = input('what is your nickname?\n')
    nickname = "TEST"
    password = None
    if nickname == 'admin':
        password = input('Plese enter the password:\n')
    c = Client(nickname,password)
    c.connectClientToServer()
