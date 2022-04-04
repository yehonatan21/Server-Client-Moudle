# Chat Server: Client - Server Moudle

**version 1.0.0**

**Structure:** 
The system 2 server moudles inheriting from server class: Discovey Server(UDP) and Chat Server(TCP).
The client is connecting to the discovery server to recive the host and port for the chat server.
After reciving the chat server host and port the client connecting to chat server.

**Run:** 
1. To run the program you need to load the discoveryServer.py first.
2. After the discoveryServer.py is running run the chatServer.py.
3. When both of the servers ars running run the client.py and connect to the chat server.

**note:**
 - The server configurations is seted to local host. you can change is in the config.ini files.

## License & Copyright

© Jonathan Shabtai