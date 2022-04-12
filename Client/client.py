import socket
import threading
import logging
from configparser import ConfigParser
from clientTraceback import clientTraceback

#TODO: send codes insted of strings to the client - JSON?
#TODO: sepeareat to coreClient and clientImplementaion

class Client():
    def __init__(self, nick, password = None): #TODO: Talk about the password
        """Reading the Configuration file, creating the class instances and creating costum logging file"""
        self.__nickname = nick
        self.__password = password
        self.__running = True
        self.__myTrace = clientTraceback()
        if(self.__myTrace.is_debug()):
            import os
            logging.debug(os.getcwd())
            logging.basicConfig(
                filename='client-debug.logs',
                level=logging.DEBUG,
                format='%(asctime)s: %(levelname)s: %(message)s'
            )
        else:
            logging.basicConfig(
                filename='client.logs',
                level=logging.INFO,
                format='%(asctime)s: %(levelname)s: %(message)s'
            )
        clientConfig = ConfigParser()
        clientConfig.read('./config.ini')
        try:
            if len(clientConfig) == 0:
                raise NameError("No configuration file")
        except:
            print("The configuration file is empty")
        self.__DISCOVERY_IP = clientConfig['DiscoveryServer']['IP']
        self.__DISCOVERY_PORT = int(clientConfig['DiscoveryServer']['PORT'])
        self.__FORMAT = clientConfig['Client']['FORMAT']
        # logging.debug(self.__DISCOVERY_IP)
        # logging.debug(self.__DISCOVERY_PORT)

    def connectClientToServer(self):
        """Connecting to discovery server to get the host and pord of the chat server and then connecting to chat server"""
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Send to server using created UDP socket
        serverAddressPort = (self.__DISCOVERY_IP, self.__DISCOVERY_PORT)
        self.__client.sendto(str.encode("KK"), serverAddressPort)
        bufferSize = 1024
        msgFromServer = self.__client.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(self.__FORMAT)
        logging.debug(f'Message from Discovery Server: "{msg}"')
        connectionInfo = msg.split(':')
        __HOST = connectionInfo[0]
        self.__PORT = int(connectionInfo[1])
        logging.debug(f'About to connect to: {__HOST}:{self.__PORT}')
        
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug(f'trying to connect to {__HOST}:{self.__PORT}')
        self.__client.connect((__HOST,self.__PORT))
        logging.debug(f'connected succefuly to {__HOST}:{self.__PORT}')
        self.__create_threads()
        
    def __printToUser(self, message):
        """Printing recived messages"""
        print(message)

    def __receive_message(self):
        """reciveing message from the server"""
        while self.__running:
            try:
                messageFromServer = self.__client.recv(1024).decode(self.__FORMAT)
                if messageFromServer == 'nickname': #TODO: make it match-case insted of if-else?
                    self.__client.send(self.__nickname.encode(self.__FORMAT))
                    messageFromServer = self.__client.recv(1024).decode(self.__FORMAT)
                    if messageFromServer  == 'PASS':
                        self.__client.send(self.__password.encode(self.__FORMAT))
                        messageFromServer = self.__client.recv(1024).decode(self.__FORMAT)
                        if messageFromServer == 'Refuse':
                            self.__printToUser('Connection refused. Wrong password!')
                            self.__running = False
                        else:
                            self.__printToUser(messageFromServer) 
                    else:
                        self.__printToUser(messageFromServer) 
                else:
                    self.__printToUser(messageFromServer) 

                if messageFromServer == ('You have discinnected successfully.' or 'Refuse' or 'You left the chat room' or 'You have been kicket from the chat room'): #TODO: get codes insted of strings
                    self.__running = False
                
                if messageFromServer == 'This nickname is already exist.Plese choose new one':
                    nickname = input("")
                    print(nickname) 
                
                if messageFromServer == '':
                    self.__printToUser('The server is down. Click enter to exit.')
                    self.__client.close()
                    self.__running = False

                if messageFromServer == 'IP':
                    self.__client.send('send'.encode(self.__FORMAT))
                    serverIP = self.__client.recv(1024).decode(self.__FORMAT)
                    self.__client.close()
                    self.__connectServer(serverIP)
            except Exception as e:
                logging.debug(e)
                self.__printToUser('An error occured!')
                self.__client.close()
                self.__running = False
                break

    def __write_message(self):
        """writeing message to the server"""
        while self.__running or message == "/exit":
            message = f'{input("")}'
            self.__client.send(message.encode(self.__FORMAT))
    
    def __connectServer(self, serverIP):
        """Connecting the client to the recived IP from discovery server"""
        self.__client.connect((serverIP,self.__PORT))

    def __create_threads(self):
        """Creating threads for reciveing and writeing messages"""
        receive_message_thread = threading.Thread(target=self.__receive_message)
        receive_message_thread.start()

        write_message_thread = threading.Thread(target=self.__write_message)
        write_message_thread.start()

if __name__ == "__main__":
    nickname = input('what is your nickname?\n')
    password = None
    if nickname == 'admin':
        password = input('Plese enter the password:\n')
    c = Client(nickname,password)
    c.connectClientToServer()
