import socket
import threading

HOST =  socket.gethostbyname('')
PORT = 5050
FORMAT = 'utf-8'
CLIENTSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nickname = input('what is your nickname?\n')
CLIENTSOCKET.connect((HOST,PORT))

def receiveMessage():
    while True:
        try:
            message = CLIENTSOCKET.recv(1024).decode(FORMAT)
            if message == 'nickname':
                CLIENTSOCKET.send(nickname.encode(FORMAT))
            else:
                print(message)
        except:
            print("An error occured!")
            CLIENTSOCKET.close()
            break   

def writeMessage():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        CLIENTSOCKET.send(message.encode(FORMAT))

receive_thread = threading.Thread(target=receiveMessage)
receive_thread.start()

write_thread = threading.Thread(target=writeMessage)
write_thread.start()