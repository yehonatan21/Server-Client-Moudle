import unittest
import sys 
# import os
# sys.path.append('C:\\Users\\User\\Desktop\\Car-Race\\Server')
sys.path.append('./Server')
from Utilities.server import Server
# print(sys.path)
# print('Current Directory: ' + os.getcwd())
# import server
# print(dir(server.Server))

class TestChatServer(unittest.TestCase):  
    
    def test_connection(self):
        s = Server()
        s.startServer()
        self.assertTrue(self.s.receiveConnections())

    def test_connection2(self):
        s = Server()
        s.startServer()
        self.assertTrue(self.s.receiveConnections())

if __name__ == "__main__":
    unittest.main()