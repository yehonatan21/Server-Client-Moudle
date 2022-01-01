import socket
import threading

HOST =  socket.gethostbyname('')
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER.bind((HOST,PORT))
SERVER.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients'connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat room!'.encode(FORMAT))
            nicknames.remove(nickname)
            break

# Main function to receive the clients connection
def receiveConnections():
    while True:
        print(f'Server is running and listening in port {PORT}...')
        client, address = SERVER.accept()
        print(f'connection is established with {str(address)}')
        client.send('nickname'.encode(FORMAT))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f'The nickname of this client is {nickname}'.encode(FORMAT))
        client.send('you are now connected!\n'.encode(FORMAT))
        broadcast(f'{nickname} has connected to the chat room!'.encode(FORMAT))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()        

if __name__ == "__main__":
    receiveConnections()