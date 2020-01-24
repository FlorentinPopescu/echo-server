from echo_client import client
import socket
import unittest
import errno
# ----------------------------------------


class EchoTestCase(unittest.TestCase):
    """tests for the echo server and client"""

    def send_message(self, message):
        """Attempt to send a message using the client

        In case of a socket error, fail and report the problem
        """
        try:
            reply = client(message)
        except (socket.error, ConnectionRefusedError) as e:
            if e.errno == 61:
                msg = "Error: {0}, is the server running?"
                self.fail(msg.format(e.strerror))
            else:
                self.fail("Unexpected Error: {0}".format(str(e)))
        return reply
        
    def test_short_message_echo(self):
        """test that a message short than 16 bytes echoes cleanly"""
        expected = "short message"
        actual = self.send_message(expected)
        self.assertEqual(
            expected,
            actual,
            "expected {0}, got {1}".format(expected, actual)
        )
    
    def test_long_message_echo(self):
        """test that a message longer than 16 bytes echoes in 16-byte chunks"""
        expected = "Four score and seven years ago our fathers did stuff"
        actual = self.send_message(expected)
        self.assertEqual(
            expected,
            actual,
            "expected {0}, got {1}".format(expected, actual)
        )
        
    @staticmethod        
    def isOpen(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.connect((ip, int(port)))     
            sock.shutdown(2)
            sock.close()
            return True
        except (socket.error, OSError, ConnectionRefusedError):
            return False
     
    @staticmethod    
    def isBusy(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try: 
            sock.bind((ip, int(port)))
            sock.shutdown(2)
            sock.close()
            return True
        except (socket.error, OSError, ConnectionRefusedError) as e:
            if e.errno == errno.EADDRINUSE:
                print("port already in use")
                return False 
            else:
                print("port cannot be reached")
                return False
    # ----------------------------------------        


if __name__ == '__main__':
    server_ip, client_ip = '127.0.0.1', 'localhost' 
    server_port = client_port = 10000
    if (EchoTestCase.isOpen(server_ip, server_port) \
        and EchoTestCase.isOpen(client_ip, client_port)):
        print("--- ports open; running tests ---")
        unittest.main()
    elif EchoTestCase.isBusy(server_ip, server_port):
        print("server port taken; check back latter or try another port")
    else:
        print("please open server port before running the tests")


# ==============================================
# ============== SAMPLE RUN ====================
# --- ports open; running tests ---
# connecting to localhost port 10000
# sending "Four score and seven years ago our fathers did stuff"
# received: "Four score and s"
# received: "even years ago o"
# received: "ur fathers did s"
# received: "tuff"
# received message = Four score and seven years ago our fathers did stuff
# closing socket
# .connecting to localhost port 10000
# sending "short message"
# received: "short message"
# received message = short message
# closing socket
# .
# ----------------------------------------------------------------------
# Ran 2 tests in 0.011s

# OK