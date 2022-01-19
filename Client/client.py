import socket
import threading
import CarRace
#TODO: opening the race from the server

HOST =  socket.gethostbyname('')
PORT = 6050
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST,PORT))


class Client():


    __nickname = input('what is your nickname?\n')
    __stop_loops = False
    if __nickname == 'admin':
        __password = input('Plese enter the password:\n')


    def __receive_message(self):
        while True:
            if self.__stop_loops:
                break
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'nickname':
                    client.send(self.__nickname.encode(FORMAT))
                    message = client.recv(1024).decode(FORMAT)
                    if message  == 'PASS':
                        client.send(self.__password.encode(FORMAT))
                        message = client.recv(1024).decode(FORMAT)
                        if message == 'Refuse':
                            print('Connection refused. Wrong password!')
                            self.__stop_loops = True
                        else:
                            print(message) 
                    else:
                        print(message) 
                else:
                    print(message) 
                if message == 'You have discinnected successfully.' and 'Refuse' and 'You left the chat room' and 'You have been kicket from the chat room': #FIXME: OR is not working
                    self.__stop_loops = True
                if message == '':
                    print('The server is down. Click enter to exit.')
                    client.close()
                    self.__stop_loops = True
                # if message ==  '/start_race':
                #     race = CarRace(racers_num)

                # if message == 'This nickname is already exist. Please send a new nickname':
                #     self.__nickname = input('The nickname you choose is already exist. Please choose new nickname:\n')
                #     client.send(self.__nickname.encode(FORMAT))
            except:
                print('An error occured!')
                client.close()
                self.__stop_loops = True

    def __write_message(self): #FIXME: how can i immediately breakthis loop like rhe recive loop without pressing the enter buttom
        while True:
            if self.__stop_loops:
                break
            message = f'{input("")}'
            client.send(message.encode(FORMAT))
    
    def create_thread(self):
        receive_thread = threading.Thread(target=self.__receive_message)
        receive_thread.start()

        write_thread = threading.Thread(target=self.__write_message)
        write_thread.start() 

c = Client()
c.create_thread()