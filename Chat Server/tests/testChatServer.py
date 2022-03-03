import unittest
import sys 
sys.path.append('./Server')
from Utilities.server import Server

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