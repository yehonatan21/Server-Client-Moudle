# Chat Server: Client - Server Moudle

**Version 1.0.0**

## Glossary
 - Discovery Server
   - Provides a discovery server across the LAN and allows clients to find the right server. 
 - Chat Server
   - The server that is responsbile on connecting people.
 - Client
   - The way 2 or more people communicate with each other.

## How it works
1. The discovery server.py is providing the host and port to the client.
2. After the host and port from the discovery server, the client is connecting to the chat server.
3. the chat server is sending the client message to all the connected clients.

## Requirements:
Python 3.8 and above

## How to run:
### Configuration
>The server configurations is set to local host. you can change this in the config.ini file thaqt is located in each directory respectivly.
### Execute
1. Start *discoveryServer.py* by running ```python discoveryServer.py```
2. Start *chatServer.py by running ```python chatServer.py```
3. Start *client.py by running ```python client.py```

## License & Copyright
© Jonathan Shabtai
